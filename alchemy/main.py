from database import SessionLocal, engine, Base
from models import Author, Post, Comment
from crud import *
from datetime import datetime


def main():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    try:
        print("Начинаем тестирование...\n")

        print("Создаём авторов...")
        author1 = create_author(session, "Анна Петрова", "anna@example.com")
        author2 = create_author(session, "Иван Сидоров", "ivan@example.com")
        print(f"{author1.name} (id={author1.id})")
        print(f"{author2.name} (id={author2.id})\n")

        print("Создаём посты...")
        post1 = create_post(session, "Первый пост", "Это содержание первого поста. Оно достаточно длинное.", author1.id, published=True)
        post2 = create_post(session, "Черновик", "Этот пост пока не опубликован.", author1.id, published=False)
        post3 = create_post(session, "Пост Ивана", "Текст от Ивана.", author2.id, published=True)
        print(f"'{post1.title}' (опубликован)")
        print(f"'{post2.title}' (черновик)")
        print(f"'{post3.title}' (опубликован)\n")

        print("Добавляем комментарии...")
        add_comment(session, post1.id, "Читатель1", "Отличная статья, очень полезно!")
        add_comment(session, post1.id, "Читатель2", "Спасибо за материал, жду продолжения.")
        add_comment(session, post1.id, "Аноним", "Коротко.")
        print("3 комментария добавлены к первому посту\n")

        print("Публикуем черновик...")
        success = update_post_status(session, post2.id, published=True)
        if success:
            print(f"'{post2.title}' теперь опубликован\n")

        print("Все опубликованные посты:")
        published = get_published_posts(session)
        for post in published:
            print(f"'{post.title}' — автор: {post.author.name}")
        print()

        print("Топ авторов по количеству постов:")
        top_authors = get_top_authors_by_posts(session, limit=3)
        for rank, (name, count) in enumerate(top_authors, 1):
            print(f"{rank}. {name}: {count} пост(ов)")
        print()

        print("Поиск автора по email...")
        found = get_author_by_email(session, "anna@example.com")
        if found:
            print(f"Найдено: {found.name}\n")
        else:
            print("Автор не найден\n")

        print("Поиск автора по имени...")
        found_by_name = get_author_by_name(session, "Иван Сидоров")
        if found_by_name:
            print(f"Найдено: {found_by_name.name}, email: {found_by_name.email}\n")
        else:
            print("Автор не найден\n")

        print("Опубликованные посты за сегодня:")
        posts_today = get_published_posts_by_date(session, datetime.now())
        for post in posts_today:
            print(f"'{post.title}' — {post.created_at}")
        print()

        print("Добавляем нескольких авторов сразу...")
        new_authors = create_authors_bulk(session, [
            {"name": "Мария Кузнецова", "email": "maria@example.com"},
            {"name": "Алексей Попов", "email": "alexey@example.com"},
        ])
        for a in new_authors:
            print(f"Создан: {a.name} (id={a.id})")
        print()

        print("Пост с комментариями:")
        result = get_post_with_comments(session, post1.id)
        if result:
            print(f"Пост: '{result['post'].title}'")
            for comment in result["comments"]:
                print(f"  — {comment.author_name}: {comment.text}")
        print()

    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()
        print("\nТестирование завершено. Сессия закрыта.")


if __name__ == "__main__":
    main()
