from mastodon import Mastodon
import typer
from datetime import datetime, timedelta, timezone

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
        breakpoint()
    return not all(reasons)


def main(instance_url: str, access_token: str):
    """
    Clean your account of slop followers
    :param instance_url: Example https://lgbtqia.space
    :access_token Must create your api from here
    """
    mastodon = Mastodon(api_base_url=instance_url, access_token=access_token)
    me = mastodon.account_verify_credentials()
    followers = mastodon.account_followers(me["id"])
    unfollow_ids = []
    # for testing 113919261711366594
    while followers := mastodon.fetch_next(followers):
        for follower in followers:
            relationship = mastodon.account_relationships(follower['id'])[0]
            if relationship['following'] and relationship['followed_by']:
                continue

            if is_account_slop(follower):
                unfollow_ids.append(follower["id"])
                print(follower['acct'])

    # Uncomment when is_account_slop is refined
    # for follower_id in unfollow_ids:
    #     mastodon.account_remove_from_followers(follower_id)


if __name__ == "__main__":
    typer.run(main)
