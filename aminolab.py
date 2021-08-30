#Library created by LilZevi.
#I have not tested some functions. 
#I tested only auth, follow_user, unfollow_user
import requests
import json
import random
import string
from utils import headers

class Client():
	def __init__(self, deviceId: str = "22717F5C01029F06DAED62B82F001AAB42333CD930C7936EC7B253594887BA6CE6820148ED69CBF2D0"):
		self.api = "https://aminoapps.com/api"
		self.headers = headers.Headers(deviceId=deviceId).headers
		self.deviceId = deviceId
		self.userId = None
		self.sid = None

	def generate_captcha(self):
		value = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + "_-", k=462)).replace("--", "-")
		return value
        
    #thanks for LynxN1 for this
	def auth(self, email: str, password: str):
		data = {
		"auth_type": 0,
		"email": email,
		"recaptcha_challenge": self.generate_captcha(),
		"recaptcha_version": "v3",
		"secret": password
		}
		request = requests.post(f"{self.api}/auth", json=data)
		self.headers = request.headers
		self.sid = request.headers["set-cookie"]
		self.userId = request.json()["result"]["uid"]
		try:
			self.sid = self.sid[0: self.sid.index(";")]
		except:	pass
		headers.sid = self.sid
		headers.userId = self.userId
		self.headers = headers.Headers(sid=self.sid, deviceId=self.deviceId).headers
		return request.json()
		
	def add_chat_message(self, ndcId, threadId, message):
		data = {
		"ndcId": f"x{ndcId}",
		"threadId": threadId,
		"content": message,
		"mediaType": 0,
		"type": 0,
		"sendFailed": False,
		"clientRefId": 0
		}
		request = requests.post(f"{self.api}/add-chat-message", json=data, headers=self.headers)
		return request.json()
	
	def submit_comment(self, ndcId, message, userId: str = None, blogId: str = None, wikiId: str = None):
		data = {"content": message, "ndcId": ndcId}
		if blogId: data["postType"] = "blog"; postId = blogId
		if wikiId: data["postType"] = "wiki"; postId = wikiId
		if userId: data["postType"] = "user"; postId = userId
		data["postId"] = postId
		request = requests.post(f"{self.api}/submit_comment", json=data, headers=self.headers)
		return request.json()
		
	def join_thread(self, ndcId, threadId):
		data = {"ndcId": f"x{ndcId}", "threadId": threadId}
		request = requests.post(f"{self.api}/join-thread", json=data, headers=self.headers)
		return request.json()
		
	def leave_thread(self, ndcId, threadId):
		data = {"ndcId": f"x{ndcId}", "threadId": threadId}
		request = requests.post(f"{self.api}/leave-thread", json=data, headers=self.headers)
		return request.json()
		
	def members_in_thread(self, ndcId, threadId, start: int = 0, size: int = 10):
		data = {
		"ndcId": f"x{ndcId}",
		"size": size,
		"start": start,
		"threadId": threadId,
		"type": "default"
		}
		request = requests.get(f"{self.api}/members-in-thread", json=data, headers=self.headers)
		return request.json()
	
	def follow_user(self, ndcId, followee_id: str):
		data = {"followee_id": followee_id, "ndcId": f"x{ndcId}"}
		request = requests.post(f"{self.api}/follow-user", json=data, headers=self.headers)
		return request.json()
	
	def unfollow_user(self, ndcId, followee_id: str):
		data = {"followee_id": followee_id, "follower_id": headers.userId, "ndcId": f"x{ndcId}"}
		request = requests.post(f"{self.api}/unfollow-user", json=data, headers=self.headers)
		return request.json()
		
	def create_chat_thread(self, ndcId, message, userId: str):
		data = {
		"initialMessageContent": message,
		"inviteeUids": [userId],
		"ndcId": ndcId,
		"type": 0
		}
		request = requests.post(f"{self.api}/create-chat-thread", json=data, headers=self.headers)
		return request.json()
	
	def vote(self, ndcId, blogId: str = None, wikiId: str = None):
		data = {"ndcId": ndcId}
		if blogId: data["logType"] = "blog"; data["postType"] = "blog"; postId = blogId
		if wikiId: data["logType"] = "wiki"; data["postType"] = "wiki"; postId = wikiId
		data["postId"] = postId
		request = requests.post("https://aminoapps.com/api/vote", json=data, headers=self.headers)
		return request.json()
	
	def unvote(self, ndcId, blogId: str = None, wikiId: str = None):
		data = {"ndcId": ndcId}
		if blogId: data["logType"] = "blog"; data["postType"] = "blog"; postId = blogId
		if wikiId: data["logType"] = "wiki"; data["postType"] = "wiki"; postId = wikiId
		data["postId"] = postId
		request = requests.post("https://aminoapps.com/api/unvote", json=data, headers=self.headers)
		return request.json()
	
	#function post_blog():
		
	def get_web_socket_url(self):
		request = requests.get(f"{self.api}/chat/web-socket-url", headers=self.headers)