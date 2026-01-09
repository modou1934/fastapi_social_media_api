from app import schemas 
import pytest
import jwt
from app.config import settings
from app.utils import verify_password



def test_root(client):
    response = client.get("/")
    assert response.json().get("message") == 'Welcome to NotiClient: the best AI app for financial advisors!!!!!'
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/",json={"username":"useradmin","email":"smabcisse@gmail.com","password":"password123"})
    print(response.json())
    new_user = schemas.UserResponse(**response.json())#validiamo la risposta usando il pydantic model che abbiamo creato e visto che si tratta di un dizionario lo spacchettiamo usando **
    assert new_user.email == "smabcisse@gmail.com"
    assert response.status_code == 201

def test_read_user(client,test_user):
    response= client.get(f"/users/{test_user["id"]}")
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "cisse@gmail.com"
    assert new_user.username == "useradmin"
    assert response.status_code == 200


def test_login_user(client,test_user):
    response = client.post("/login/",json={"email":test_user["email"],"password":test_user["password"]})
    login_res = schemas.Token(**response.json())#validiamo la risposta usando il pydantic model che abbiamo creato e visto che si tratta di un dizionario lo spacchettiamo usando **
    decode_jwt = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = decode_jwt.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email,password,status_code",[
    ("bhjsd@dfh.c","uuafdjh",403),
    ("bhjswwed@dfh.c","uusadaafdjh",403),
    ("bhfaa@dfh.c","uuafdadsjh",403),
    ("bhadasdjsd@das.c","uuafd<zxcjh",403),
    ("bhjsadd@ddsaadfh.c","uuadadfdjh",403),
    ("bhjsadd@ddsaadfh.c",None,422),
    (None,"sdsa",422),
])
def test_incorrect_login(test_user,client,email,password,status_code):
    response = client.post("/login/",json={"email":email,"password":password})
    assert response.status_code == status_code
    #assert response.json().get("detail") == "Invalid credentials"

