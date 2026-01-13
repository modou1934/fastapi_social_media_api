import pytest
from app import models


@pytest.fixture(scope="module")
def test_like(test_posts,session,test_user):
    new_vote= models.Likes(post_id=test_posts[7].id,user_id=test_user["id"])
    session.add(new_vote)
    session.commit()

def test_likes_own_post(authorized_client,test_posts):
    res = authorized_client.post("/likes/",json={"post_id":test_posts[3].id,"dir":1})
    assert res.status_code == 400
def test_likes_other_user_post(authorized_client,test_posts):
    res = authorized_client.post("/likes/",json={"post_id":test_posts[8].id,"dir":1})
    assert res.status_code == 201


def test_likes_twice_post(authorized_client,test_posts,test_like):
    res = authorized_client.post("/likes/",json={"post_id":test_posts[7].id,"dir":1})
    print(res.json())
    assert res.status_code == 400

def test_delete_likes_post(authorized_client,test_posts,test_like):
    res = authorized_client.post("/likes/",json={"post_id":test_posts[7].id,"dir":0})
    assert res.status_code == 201

def test_delete_not_existing_likes_post(authorized_client,test_posts):
    res = authorized_client.post("/likes/",json={"post_id":test_posts[7].id,"dir":0})
    assert res.status_code == 404

def test_like_not_existing_post(authorized_client):
    res = authorized_client.post("/likes/",json={"post_id":62624354,"dir":0})
    assert res.status_code == 404
def test_unauthorized_user_likes_other_user_post(client,test_posts):
    res = client.post("/likes/",json={"post_id":test_posts[8].id,"dir":1})
    print(res.json())
    assert res.status_code == 401
