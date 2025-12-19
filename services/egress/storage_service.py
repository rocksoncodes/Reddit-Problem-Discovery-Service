from sqlalchemy.orm import sessionmaker
from database.models import Post, Comment
from database.engine import database_engine
from utils.helpers import ensure_data_integrity
from utils.logger import logger


class StorageService:
    def __init__(self):
        self.SessionLocal = sessionmaker(bind=database_engine)
        
    def store_posts(self, reddit_data):

        session = self.SessionLocal()
        stored_posts = 0
        
        validated_posts = ensure_data_integrity(session, reddit_data)

        try:
            for post_data in reddit_data.get("posts", []):
                if post_data["submission_id"] in validated_posts:
                    post = Post(
                        submission_id = post_data["submission_id"],
                        subreddit = post_data.get("subreddit", ""),
                        title = post_data.get("title", ""),
                        body = post_data.get("body", ""),
                        upvote_ratio = post_data.get("upvote_ratio", 0.0),
                        score = post_data.get("score", 0),
                        number_of_comments = post_data.get("number_of_comments", 0),
                        post_url = post_data.get("post_url","")
                    )
                    session.add(post)
                    stored_posts += 1

            session.commit()
            logger.info(f"Stored {stored_posts} posts.")
            return {"posts_stored": stored_posts}

        except Exception as e:
            session.rollback()
            logger.error(f"Error storing Reddit posts: {e}", exc_info=True)

        finally:
            session.close()
            
        
    def store_comments(self, reddit_data: dict):

        session = self.SessionLocal()
        stored_comments = 0
        
        try:
            for comment_data in reddit_data.get("comments", []):
                comment = Comment(
                    submission_id = comment_data["submission_id"],
                    title = comment_data.get("title", ""),
                    subreddit = comment_data.get("subreddit", ""),
                    author = comment_data.get("author", ""),
                    body = comment_data.get("body", ""),
                    score = comment_data.get("score", 0)
                )
                session.add(comment)
                stored_comments += 1
                    
            session.commit()
            logger.info(f"Stored {stored_comments} comments.")
            return {"comments_stored": stored_comments}
        
        except Exception as e:
            session.rollback()
            logger.error(f"Error storing Reddit comments: {e}", exc_info=True)
            return {"error": str(e)}

        finally:
            session.close()