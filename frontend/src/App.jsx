import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";

import Login from "./pages/Login";
import Home from "./pages/Home";
import Project from "./pages/Project";

function App() {
  const [token, setToken] = useState(null);

  // ローカルストレージから token を取得
  useEffect(() => {
    const t = localStorage.getItem("token");
    setToken(t);
  }, []);

  // 認証が必要なルート用コンポーネント
  const ProtectedRoute = ({ children }) => {
    if (!token) return <Navigate to="/login" replace />;
    return children;
  };

  return (
    <BrowserRouter>
      <Routes>
        {/* ログイン画面 */}
        <Route
          path="/login"
          element={<Login onLogin={() => setToken(localStorage.getItem("token"))} />}
        />

        {/* ホーム画面（認証必須） */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />

        {/* プロジェクト画面（認証必須） */}
        <Route
          path="/projects/:id"
          element={
            <ProtectedRoute>
              <Project />
            </ProtectedRoute>
          }
        />

        {/* その他のURLはホームへリダイレクト */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;