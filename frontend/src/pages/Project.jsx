import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getProject, getTasksByProject, deleteTask, createTask } from "../api";

function Project() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [project, setProject] = useState(null);
    const [tasks, setTasks] = useState([]);
    const [newTaskTitle, setNewTaskTitle] = useState("");

    useEffect(() => {
        fetchData();
    }, [id]);

    const fetchData = async () => {
        try {
            const projRes = await getProject(id);
            setProject(projRes.data);

            const tasksRes = await getTasksByProject(id);
            setTasks(tasksRes.data);
        } catch (err) {
            alert("プロジェクト取得失敗: " + (err.response?.data?.detail || err.message));
        }
    };

    const handleDeleteTask = async (taskId) => {
        if (!window.confirm("本当に削除しますか？")) return;

        try {
            await deleteTask(taskId);
            fetchData();
        } catch (err) {
            alert("削除失敗: " + (err.response?.data?.detail || err.message));
        }
    };

    const handleAddTask = async (e) => {
        e.preventDefault();

        if (!newTaskTitle.trim()) return;

        try {
            await createTask({
                title: newTaskTitle,
                project_id: id
            });

            setNewTaskTitle("");
            fetchData();
        } catch (err) {
            alert("タスク作成失敗: " + (err.response?.data?.detail || err.message));
        }
    };

    if (!project) return <div>Loading...</div>;

    return (
        <div style={{ maxWidth: "600px", margin: "0 auto" }}>
            <button onClick={() => navigate("/")}>
                ホームに戻る
            </button>

            <h1>{project.name}</h1>
            <p>{project.description}</p>

            <h2>タスク一覧</h2>

            <ul>
                {tasks.map((t) => (
                    <li key={t.id} style={{ marginBottom: "8px" }}>
                        {t.title} - {t.status} - 優先度: {t.priority}

                        <button
                            style={{ marginLeft: "8px", color: "red" }}
                            onClick={() => handleDeleteTask(t.id)}
                        >
                            削除
                        </button>
                    </li>
                ))}
            </ul>

            <h3>新規タスク追加</h3>

            <form onSubmit={handleAddTask}>
                <input
                    type="text"
                    placeholder="新規タスク名"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    required
                    style={{ marginRight: "8px" }}
                />

                <button type="submit">
                    追加
                </button>
            </form>
        </div>
    );
}

export default Project;