from sqlalchemy.orm import Session
from typing import List, Dict, Tuple, Any
from database.models import Comment, Post
from utils.logger import logger


def serialize_comment(comment: Comment) -> Dict:
    return {
        "comment_id": comment.id,
        "post_key": comment.submission_id,
        "body": comment.body,
        "author": comment.author,
        "score": comment.score,
    }


def serialize_post(post: Post, comments: List[Dict]) -> Dict:
    return {
        "post_number": post.id,
        "post_key": post.submission_id,
        "subreddit": post.subreddit,
        "title": post.title,
        "body": post.body,
        "comments": comments,
    }


def get_comments_for_post(session, post_id: str) -> Tuple[List[Dict], int]:
    comments = (
        session.query(Comment)
        .filter(Comment.submission_id == post_id)
        .all()
    )

    comment_records = []
    count = 0
    for comment in comments:
        comment_records.append(serialize_comment(comment))
        count += 1

    return comment_records, count


def get_comments_from_submission(reddit, submission_id: str, comment_limit: int) -> List[Dict[str, Any]]:
    """
    Fetch and format comments from a single Reddit submission.

    Args:
        reddit: The Reddit client instance.
        submission_id: The Reddit submission ID to fetch comments from.
        comment_limit: Max number of comments to retrieve.

    Returns:
        List[Dict[str, Any]]: List of comment data dictionaries.
    """
    comments_collected = []

    submission = reddit.submission(id=submission_id)
    submission.comments.replace_more(limit=0)

    comments = submission.comments.list()
    if comment_limit:
        comments = comments[:comment_limit]

    for comment in comments:
        if not comment.body or comment.body in ("[deleted]", "[removed]"):
            continue

        comment_data: Dict[str, Any] = {
            "submission_id": submission.id,
            "title": submission.title,
            "subreddit": submission.subreddit.display_name,
            "author": str(comment.author) if comment.author else "Unknown",
            "body": comment.body,
            "score": comment.score
        }
        comments_collected.append(comment_data)

    return comments_collected


def get_posts_from_subreddit(
        reddit,
        subreddit_name: str,
        post_limit: int,
        min_upvote_ratio: float,
        min_score: int,
        min_comments: int
) -> List[Dict[str, Any]]:
    """
    Fetch and filter posts from a single subreddit.

    Args:
        reddit: The Reddit client instance.
        subreddit_name: The name of the subreddit to fetch posts from.
        post_limit: Max number of posts to retrieve.
        min_upvote_ratio: Minimum upvote ratio to include a post.
        min_score: Minimum score to include a post.
        min_comments: Minimum number of comments to include a post.

    Returns:
        List[Dict[str, Any]]: List of post data dictionaries.
    """
    posts = []

    subreddit_posts = list(reddit.subreddit(subreddit_name).hot(limit=post_limit))
    logger.info(f"Retrieved {len(subreddit_posts)} posts from r/{subreddit_name}.")

    for submission in subreddit_posts:
        if (
            submission.upvote_ratio >= min_upvote_ratio
            and submission.score >= min_score
            and submission.num_comments >= min_comments
            and not submission.stickied
        ):
            post_data: Dict[str, Any] = {
                "subreddit": subreddit_name,
                "submission_id": submission.id,
                "title": submission.title,
                "body": submission.selftext,
                "upvote_ratio": submission.upvote_ratio,
                "score": submission.score,
                "number_of_comments": submission.num_comments,
                "post_url": submission.url
            }
            posts.append(post_data)

    return posts


def ensure_data_integrity(session: Session, reddit_data) -> list:
    """
    Returns a list of submission_ids that do NOT exist in the database.
    """
    posts_list = reddit_data.get("posts", [])
    submission_ids_from_posts = []

    for post in posts_list:
        submission_ids_from_posts.append(post["submission_id"])

    if len(submission_ids_from_posts) == 0:
        return []

    query_results = session.query(Post.submission_id).filter(Post.submission_id.in_(submission_ids_from_posts)).all()

    existing_submission_ids = set()
    for record in query_results:
        existing_submission_ids.add(record[0])

    new_submission_ids = []
    for submission_id in submission_ids_from_posts:
        if submission_id not in existing_submission_ids:
            new_submission_ids.append(submission_id)

    return new_submission_ids