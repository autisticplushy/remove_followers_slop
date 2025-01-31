from mastodon import Mastodon, streaming
import typer
from datetime import datetime, timedelta, timezone
from functools import partial

MINIMUM_AGE = datetime.now(timezone.utc) - timedelta(days=5)
MINIMUM_TOOTS = 30
MINIMUM_FOLLOWER_COUNT = 10
MINIMUM_FOLLOWING_COUNT = 10
MINIMUM_BIO_LENGTH = 10
MINIMUM_STATUSES_COUNT = 30


# ATM this function is not very refined
# Careful
def is_account_slop(follower: dict):
    """
    Filters account data to determine if it's slop.

    :param follower: dict with the user profile
    """
    reasons = [
            follower["created_at"] > MINIMUM_AGE,
            follower["followers_count"] < MINIMUM_FOLLOWER_COUNT,
            follower["following_count"] < MINIMUM_FOLLOWING_COUNT,
            len(follower["note"]) < MINIMUM_BIO_LENGTH,
            follower["statuses_count"] < MINIMUM_STATUSES_COUNT,
            "missing.png" in follower["avatar"], # Default avatar in mastodon
        ]

    if True in reasons:
        print(reasons)
        print(follower)
    return not all(reasons)


def is_notification_follow(mastodon, notification):
    if notification['type'] == "follow":
        print("I have been followed")
        follower = mastodon.account(notification['account'])
        # check if user is slop
        print(is_account_slop(follower))

    print(notification)


def main(instance_url: str, access_token: str):
    """
    Stream the timeline

    :param instance_url: Example https://lgbtqia.space
    :access_token Must create your api from here
    """
    mastodon = Mastodon(api_base_url=instance_url, access_token=access_token)
    listener = streaming.CallbackStreamListener(
        notification_handler = partial(is_notification_follow, mastodon)
    )
    print("Streaming!")
    mastodon.stream_user(
        listener,
        # run_async = True,
        # reconnect_async = True
    )


if __name__ == "__main__":
    typer.run(main)
