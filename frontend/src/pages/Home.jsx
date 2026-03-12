import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getProjects, createProject, deleteProject } from "../api";

function Home() {
    const [projects, setProjects] = useState([]);
    const [newProjectName, setNewProjectName] = useState("");
    const [newProjectDesc, setNewProjectDesc] = useState("");
    const navigate = useNavigate();

    // プロジェクト一覧取得
    useEffect(() => {
        fetchProjects();
    }, []);

    const fetchProjects = async () => {
        try {
            const res = await getProjects();
            setProjects(res.data);
        } catch (err) {
            alert("プロジェクト取得失敗: " + err.response?.data?.detail || err.message);
        }
    };

    // ログアウト処理
    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login", { replace: true });
    };

    // プロジェクト削除
    const handleDelete = async (id) => {
        if (!window.confirm("本当に削除しますか？")) return;

        try {
            await deleteProject(id);
            fetchProjects();
        } catch (err) {
            alert("削除失敗: " + err.response?.data?.detail || err.message);
        }
    };

    // 新規プロジェクト作成
    const handleCreate = async (e) => {
        e.preventDefault();
        if (!newProjectName.trim()) {
            alert("プロジェクト名を入力してください");
            return;
        }

        try {
            await createProject({ name: newProjectName, description: newProjectDesc });
            setNewProjectName("");
            setNewProjectDesc("");
            fetchProjects();
        } catch (err) {
            alert("作成失敗: " + err.response?.data?.detail || err.message);
        }
    };

    return (
        <div style={{ maxWidth: "600px", margin: "0 auto" }}>
            <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h1>プロジェクト一覧</h1>
                <button onClick={handleLogout}>ログアウト</button>
            </header>

            {/* 新規プロジェクト作成フォーム */}
            <form onSubmit={handleCreate} style={{ margin: "16px 0" }}>
                <input
                    type="text"
                    placeholder="プロジェクト名"
                    value={newProjectName}
                    onChange={(e) => setNewProjectName(e.target.value)}
                    required
                    style={{ marginRight: "8px" }}
                />
                <input
                    type="text"
                    placeholder="説明（任意）"
                    value={newProjectDesc}
                    onChange={(e) => setNewProjectDesc(e.target.value)}
                    style={{ marginRight: "8px" }}
                />
                <button type="submit">作成</button>
            </form>

            {/* プロジェクト一覧 */}
            <ul>
                {projects.map((p) => (
                    <li key={p.id} style={{ marginBottom: "8px" }}>
                        <button
                            style={{ marginRight: "8px" }}
                            onClick={() => navigate(`/projects/${p.id}`)}
                        >
                            {p.name}
                        </button>
                        <button
                            onClick={() => handleDelete(p.id)}
                            style={{ color: "red" }}
                        >
                            削除
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Home;