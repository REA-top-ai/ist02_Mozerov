import os
import hashlib
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from colorama import init, Fore, Style

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean, func, desc
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


load_dotenv()
init(autoreset=True)


DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "news_analyzer")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь: один пользователь → много новостей
    news = relationship("News", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username='{self.username}')>"


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    source = Column(String(100))
    url = Column(String(500))
    published_at = Column(DateTime)
    saved_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="news")
    analysis = relationship("Analysis", back_populates="news", cascade="all, delete-orphan", uselist=False)

    def __repr__(self):
        return f"<News(title='{self.title[:50]}')>"


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    sentiment = Column(String(20))
    summary = Column(Text)
    tags = Column(String(200))
    analyzed_at = Column(DateTime, default=datetime.utcnow)

    news_id = Column(Integer, ForeignKey("news.id"), nullable=False, unique=True)

    news = relationship("News", back_populates="analysis")

    def __repr__(self):
        return f"<Analysis(sentiment='{self.sentiment}')>"



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(session, username, password):
    """Создаёт нового пользователя"""
    new_user = User(username=username, password_hash=hash_password(password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_user_by_username(session, username):
    """Ищет пользователя по имени"""
    return session.query(User).filter(User.username == username).first()


def create_news(session, user_id, title, description, source, url, published_at):
    """Создаёт новость"""
    new_news = News(
        user_id=user_id,
        title=title,
        description=description,
        source=source,
        url=url,
        published_at=published_at
    )
    session.add(new_news)
    session.commit()
    session.refresh(new_news)
    return new_news


def create_analysis(session, news_id, sentiment, summary, tags):
    """Создаёт анализ для новости"""
    new_analysis = Analysis(
        news_id=news_id,
        sentiment=sentiment,
        summary=summary,
        tags=tags
    )
    session.add(new_analysis)
    session.commit()
    session.refresh(new_analysis)
    return new_analysis


def get_analysis_with_news(session, user_id, limit=10):
    """Возвращает список кортежей (News, Analysis) для пользователя"""
    return (session.query(News, Analysis)
            .join(Analysis, News.id == Analysis.news_id)
            .filter(News.user_id == user_id)
            .order_by(News.saved_at.desc())
            .limit(limit)
            .all())


def get_top_users_by_news(session, limit=5):
    """Топ пользователей по количеству новостей (аналитическая функция)"""
    return (session.query(
        User.username,
        func.count(News.id).label('news_count')
    )
            .join(News, User.id == News.user_id)
            .group_by(User.id)
            .order_by(desc('news_count'))
            .limit(limit)
            .all())



def safe_string(value, max_length=100):
    if value is None:
        return "Нет данных"
    return str(value)


def fetch_news():
    """Загружает новости из NewsAPI"""
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            news_list = []
            for article in articles:
                title = article.get('title')
                if title is None or title == "[Removed]":
                    continue
                news_list.append({
                    'title': safe_string(article.get('title'), 300),
                    'description': safe_string(article.get('description'), 1000),
                    'source': safe_string(article.get('source', {}).get('name'), 100),
                    'url': safe_string(article.get('url'), 500),
                    'published_at': article.get('publishedAt', datetime.now().isoformat())
                })
            print(Fore.GREEN + f"📰 Загружено {len(news_list)} новостей")
            return news_list
        else:
            print(Fore.RED + f"❌ Ошибка API новостей: {response.status_code}")
            return []
    except Exception as e:
        print(Fore.RED + f"❌ Ошибка загрузки новостей: {e}")
        return []


def analyze_news_with_mistral(title, description):
    """Анализирует новость через Mistral AI"""
    if len(description) > 500:
        description = description[:500] + "..."
    prompt = f"""Проанализируй следующую новость. Ответь строго в формате JSON:
{{
    "sentiment": "positive/negative/neutral",
    "summary": "Краткое резюме одним предложением на русском (максимум 20 слов)",
    "tags": "тег1, тег2, тег3 (максимум 5 тегов)"
}}
Название: {title}
Описание: {description}"""
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        content = content.strip('`').replace('json\n', '').strip()
        result = json.loads(content)
        return {'sentiment': result.get('sentiment', 'neutral'),
                'summary': result.get('summary', 'Нет резюме'),
                'tags': result.get('tags', 'общее')}
    except Exception as e:
        print(Fore.RED + f"❌ Ошибка Mistral: {e}")
        return {'sentiment': 'unknown', 'summary': 'Ошибка анализа', 'tags': 'ошибка'}


def print_analysis_result(news, analysis, index):
    """Выводит результат анализа в терминал"""
    sentiment_colors = {'positive': Fore.GREEN, 'negative': Fore.RED, 'neutral': Fore.YELLOW, 'unknown': Fore.MAGENTA}
    sentiment_color = sentiment_colors.get(analysis['sentiment'], Fore.WHITE)
    print("\n" + "=" * 70)
    print(f"{Fore.CYAN}📰 НОВОСТЬ #{index}")
    print(f"{Fore.WHITE}📌 Заголовок: {safe_string(news.get('title'), 80)}")
    print(f"{Fore.WHITE}📝 Описание: {safe_string(news.get('description'), 100)}...")
    print(f"{Fore.WHITE}🔗 Источник: {safe_string(news.get('source'), 50)}")
    print(f"\n{Fore.MAGENTA}🤖 АНАЛИЗ ОТ MISTRAL AI:")
    print(f"{sentiment_color}📊 Тональность: {analysis['sentiment'].upper()}")
    print(f"{Fore.BLUE}📋 Резюме: {analysis['summary']}")
    print(f"{Fore.CYAN}🏷️ Теги: {analysis['tags']}")
    print("=" * 70)



def main():
    # Создаём таблицы, если их нет
    Base.metadata.create_all(bind=engine)

    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "🤖 AI-АССИСТЕНТ ДЛЯ АНАЛИЗА НОВОСТЕЙ (PostgreSQL + SQLAlchemy)")
    print(Fore.CYAN + "=" * 50)

    while True:
        print("\n1️⃣ Вход")
        print("2️⃣ Регистрация")
        print("3️⃣ Выход")
        choice = input(Fore.YELLOW + "Выберите действие: ").strip()

        if choice == "1":
            username = input("👤 Логин: ")
            password = input("🔒 Пароль: ")
            session = SessionLocal()
            user = get_user_by_username(session, username)
            session.close()

            if user and user.password_hash == hash_password(password):
                print(Fore.GREEN + f"✅ Добро пожаловать, {username}!")
                user_id = user.id

                while True:
                    print(f"\n{Fore.CYAN}ГЛАВНОЕ МЕНЮ")
                    print("1️⃣ Загрузить и проанализировать последние новости")
                    print("2️⃣ Показать историю анализов")
                    print("3️⃣ Топ пользователей по количеству новостей (аналитика)")
                    print("4️⃣ Выйти из аккаунта")
                    action = input(Fore.YELLOW + "Выберите действие: ").strip()

                    if action == "1":
                        print(Fore.CYAN + "\n📡 Загрузка новостей...")
                        news_list = fetch_news()
                        if news_list:
                            session = SessionLocal()
                            for i, news_item in enumerate(news_list, 1):
                                print(Fore.YELLOW + f"\n🔄 Анализ новости {i}/{len(news_list)}...")
                                analysis = analyze_news_with_mistral(news_item['title'], news_item['description'])
                                try:
                                    pub_date = datetime.fromisoformat(news_item['published_at'].replace('Z', '+00:00'))
                                except:
                                    pub_date = datetime.utcnow()
                                new_news = create_news(session, user_id,
                                                       news_item['title'], news_item['description'],
                                                       news_item['source'], news_item['url'], pub_date)
                                create_analysis(session, new_news.id,
                                                analysis['sentiment'], analysis['summary'], analysis['tags'])
                                print_analysis_result(news_item, analysis, i)
                            session.close()
                            print(Fore.GREEN + f"\n✅ Все новости сохранены в PostgreSQL!")
                        else:
                            print(Fore.RED + "❌ Не удалось загрузить новости.")

                    elif action == "2":
                        session = SessionLocal()
                        results = get_analysis_with_news(session, user_id, limit=10)
                        session.close()
                        if not results:
                            print(Fore.YELLOW + "📭 Нет сохранённых новостей")
                        else:
                            print(Fore.CYAN + "\n📚 ПОСЛЕДНИЕ 10 НОВОСТЕЙ:")
                            for i, (news, analysis) in enumerate(results, 1):
                                sentiment_color = Fore.GREEN if analysis.sentiment == 'positive' else Fore.RED if analysis.sentiment == 'negative' else Fore.YELLOW
                                print(f"\n{i}. {Fore.WHITE}{safe_string(news.title, 60)}")
                                print(f"   {sentiment_color}Тональность: {analysis.sentiment}")
                                print(f"   {Fore.BLUE}Резюме: {safe_string(analysis.summary, 80)}")
                                print(f"   {Fore.CYAN}Теги: {safe_string(analysis.tags, 50)}")
                                print(f"   {Fore.YELLOW}📅 {news.saved_at.strftime('%Y-%m-%d %H:%M')}")

                    elif action == "3":
                        session = SessionLocal()
                        top_users = get_top_users_by_news(session)
                        session.close()
                        print(Fore.CYAN + "\n🏆 ТОП ПОЛЬЗОВАТЕЛЕЙ ПО КОЛИЧЕСТВУ НОВОСТЕЙ:")
                        for rank, (username, count) in enumerate(top_users, 1):
                            print(f"   {rank}. {username}: {count} новостей")

                    elif action == "4":
                        print(Fore.YELLOW + "👋 До свидания!")
                        break
                    else:
                        print(Fore.RED + "❌ Неверный выбор!")
            else:
                print(Fore.RED + "❌ Неверное имя пользователя или пароль!")

        elif choice == "2":
            username = input("👤 Придумайте логин: ")
            password = input("🔒 Придумайте пароль: ")
            confirm = input("🔒 Подтвердите пароль: ")
            if password == confirm:
                session = SessionLocal()
                existing = get_user_by_username(session, username)
                if existing:
                    print(Fore.RED + "❌ Пользователь уже существует!")
                else:
                    create_user(session, username, password)
                    print(Fore.GREEN + f"✅ Пользователь {username} зарегистрирован!")
                session.close()
            else:
                print(Fore.RED + "❌ Пароли не совпадают!")

        elif choice == "3":
            print(Fore.YELLOW + "👋 До свидания!")
            break
        else:
            print(Fore.RED + "❌ Неверный выбор!")


if __name__ == "__main__":
    main()