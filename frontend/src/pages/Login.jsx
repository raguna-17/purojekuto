import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api";

function Login({ onLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await login({ email, password });
            localStorage.setItem("token", res.data.access_token);
            onLogin();           // App にログイン状態を通知
            navigate("/");       // ホーム画面へ遷移
        } catch (err) {
            alert("ログイン失敗: " + err.response?.data?.detail || err.message);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button type="submit">Login</button>
        </form>
    );
}

export default Login;