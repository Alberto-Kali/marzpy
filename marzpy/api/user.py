from .send_requests import *
import json

async def delete_if_exist(dic,keys:list):
    for key in keys:
        if key in dic:
            del dic[key]
    return dic

class User:
    def __init__(
        self,
        username: str,
        proxies: dict,
        inbounds: dict,  
        data_limit: float,
        data_limit_reset_strategy: str = "no_reset",
        status="",
        expire: float = 0,
        used_traffic=0,
        lifetime_used_traffic=0,
        created_at="",
        links=[],
        subscription_url="",
        excluded_inbounds={},
        note="",
        on_hold_timeout=0,
        on_hold_expire_duration=0,
        sub_updated_at=0,
        online_at=0,
        sub_last_user_agent: str = "",
        auto_delete_in_days: int = 0,
        **kwargs
    ):
        self.username = username
        self.proxies = proxies
        self.inbounds = inbounds
        self.expire = expire
        self.data_limit = data_limit
        self.data_limit_reset_strategy = data_limit_reset_strategy
        self.status = status
        self.used_traffic = used_traffic
        self.lifetime_used_traffic = lifetime_used_traffic
        self.created_at = created_at
        self.links = links
        self.subscription_url = subscription_url
        self.excluded_inbounds = excluded_inbounds
        self.note = note
        self.on_hold_timeout = on_hold_timeout
        self.on_hold_expire_duration = on_hold_expire_duration
        self.sub_last_user_agent = sub_last_user_agent
        self.online_at = online_at
        self.sub_updated_at = sub_updated_at
        self.auto_delete_in_days = auto_delete_in_days
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        """Serialize the User object to a dictionary suitable for JSON encoding"""
        return {
            "username": self.username,
            "proxies": self.proxies,
            "inbounds": self.inbounds,
            "expire": self.expire,
            "data_limit": self.data_limit,
            "data_limit_reset_strategy": self.data_limit_reset_strategy,
            "status": self.status,
            "used_traffic": self.used_traffic,
            "lifetime_used_traffic": self.lifetime_used_traffic,
            "created_at": self.created_at,
            "links": self.links,
            "subscription_url": self.subscription_url,
            "excluded_inbounds": self.excluded_inbounds,
            "note": self.note,
            "on_hold_timeout": self.on_hold_timeout,
            "on_hold_expire_duration": self.on_hold_expire_duration,
            "sub_last_user_agent": self.sub_last_user_agent,
            "online_at": self.online_at,
            "sub_updated_at": self.sub_updated_at,
            "auto_delete_in_days": self.auto_delete_in_days
        }

    def to_json(self):
        """Convert the object to a JSON string"""
        return json.dumps(self.to_dict())

    def __str__(self):
        """Returns a readable string representation of the User object"""
        attrs = [
            f"username='{self.username}'",
            f"status='{self.status}'",
            f"data_limit={self.data_limit}",
            f"expire={self.expire}",
            f"used_traffic={self.used_traffic}",
            f"lifetime_used_traffic={self.lifetime_used_traffic}",
            f"created_at='{self.created_at}'",
            f"subscription_url='{self.subscription_url}'",
            f"note='{self.note}'",
            f"on_hold_timeout={self.on_hold_timeout}",
            f"on_hold_expire_duration={self.on_hold_expire_duration}",
            f"sub_updated_at={self.sub_updated_at}",
            f"online_at={self.online_at}",
            f"auto_delete_in_days={self.auto_delete_in_days}"
        ]
        return f"User({', '.join(attrs)})"

    def __repr__(self):
        return self.__str__()


class UserMethods:
    async def add_user(self, user: User, token: dict):
        """add new user.

        Parameters:
            user (``api.User``) : User Object

            token (``dict``) : Authorization token

        Returns: `~User`: api.User object
        """
        user.status = "active"
        if user.on_hold_expire_duration:
            user.status = "on_hold"
        request = await send_request(
            endpoint="user", token=token, method="post", data=user.__dict__
        )
        return User(**request)

    async def get_user(self, user_username: str, token: dict):
        """get exist user information by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

        Returns: `~User`: api.User object
        """
        request = await send_request(f"user/{user_username}", token=token, method="get")
        return User(**request)

    async def modify_user(self, user_username: str, token: dict, user: object):
        """edit exist user by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

            user (``api.User``) : User Object

        Returns: `~User`: api.User object
        """
        request = await send_request(f"user/{user_username}", token, "put", user.__dict__)
        return User(**request)

    async def delete_user(self, user_username: str, token: dict):
        """delete exist user by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

        Returns: `~str`: success
        """
        await send_request(f"user/{user_username}", token, "delete")
        return "success"

    async def reset_user_traffic(self, user_username: str, token: dict):
        """reset exist user traffic by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

        Returns: `~str`: success
        """
        await send_request(f"user/{user_username}/reset", token, "post")
        return "success"
    
    async def revoke_sub(self, user_username: str, token: dict):
        """Revoke users subscription (Subscription link and proxies) traffic by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

        Returns: `~str`: success
        """
        request = await send_request(f"user/{user_username}/revoke_sub", token, "post")
        return User(**request)
    
    async def get_all_users(self, token: dict, username=None, status=None):
        """get all users list.

        Parameters:
            token (``dict``) : Authorization token

        Returns:
            `~list`: list of users
        """
        endpoint = "users"
        if username:
            endpoint += f"?username={username}"
        if status:
            if "?" in endpoint:
                endpoint += f"&status={status}"
            else:
                endpoint += f"?status={status}"
        request = await send_request(endpoint, token, "get")
        user_list = [
            User(
                username="",
                proxies={},
                inbounds={},
                expire=0,
                data_limit=0,
                data_limit_reset_strategy="",
            )
        ]
        for user in request["users"]:
            user_list.append(User(**user))
        del user_list[0]
        return user_list

    async def reset_all_users_traffic(self, token: dict):
        """reset all users traffic.

        Parameters:
            token (``dict``) : Authorization token

        Returns: `~str`: success
        """
        await send_request("users/reset", token, "post")
        return "success"

    async def get_user_usage(self, user_username: str, token: dict):
        """get user usage by username.

        Parameters:
            user_username (``str``) : username of user

            token (``dict``) : Authorization token

        Returns: `~dict`: dict of user usage
        """
        return await send_request(f"user/{user_username}/usage", token, "get")["usages"]

    async def get_all_users_count(self, token: dict):
        """get all users count.

        Parameters:
            token (``dict``) : Authorization token

        Returns: `~int`: count of users
        """
        return await self.get_all_users(token)["content"]["total"]
