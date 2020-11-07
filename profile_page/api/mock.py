"""
Mock Database calls.
"""


def add_friend(source_id, new_friend_id):
    """Mock call to adding a friend to the profile."""
    return True


def accept_friend(source_id, new_friend_id):
    """Mock call to accept friend request."""
    return True


def cancel_friend_request(source_id, new_friend_id):
    """Mock call to decline friend request."""
    return True


def remove_friend(source_id, new_friend_id):
    """Mock call to remove friend from profile."""
    return True
