import axios from "axios";

export async function login(username, password) {
  try {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    const response = await axios.post("http://localhost:8000/api/user/login", params, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response.data; // 로그인 성공 메시지 반환
  } catch (error) {
    throw new Error(error.response.data.detail || "Login failed");
  }
}
