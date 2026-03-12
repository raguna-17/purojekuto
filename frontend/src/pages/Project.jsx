import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getProject, getTasksByProject, deleteTask, createTask } from "../api";
import api from "../api";

function Project() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [project, setProject] = useState(null);
    const [tasks, setTasks] = useState([]);

    // 編集対象のタスク状態
    const [editingTaskId, setEditingTaskId] = useState(null);
    const [editTitle, setEditTitle] = useState("");
    const [editStatus, setEditStatus] = useState("");
    const [editPriority, setEditPriority] = useState(1);

    const [newTaskTitle, setNewTaskTitle] = useState("");

    // データ取得
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
            alert("プロジェクト取得失敗: " + err.response?.data?.detail || err.message);
        }
    };

    // タスク削除
    const handleDeleteTask = async (taskId) => {
        if (!window.confirm("本当に削除しますか？")) return;

        try {
            await deleteTask(taskId);
            fetchData();
        } catch (err) {
            alert("削除失敗: " + err.response?.data?.detail || err.message);
        }
    };

    // 編集開始
    const startEditing = (task) => {
        setEditingTaskId(task.id);
        setEditTitle(task.title);
        setEditStatus(task.status);
        setEditPriority(task.priority);
    };

    // 編集キャンセル
    const cancelEditing = () => {
        setEditingTaskId(null);
    };

    // 編集保存
    const saveEdit = async () => {
        try {
            await api.put(`/tasks/${editingTaskId}`, {
                title: editTitle,
                status: editStatus,
                priority: editPriority,
            });
            setEditingTaskId(null);
            fetchData();
        } catch (err) {
            alert("編集失敗: " + err.response?.data?.detail || err.message);
        }
    };

    // 新規タスク追加
    const handleAddTask = async (e) => {
        e.preventDefault();
        if (!newTaskTitle.trim()) return;
        try {
            await createTask({ title: newTaskTitle, project_id: id });
            setNewTaskTitle("");
            fetchData();
        } catch (err) {
            alert("タスク作成失敗: " + err.response?.data?.detail || err.message);
        }
    };

    if (!project) return <div>Loading...</div>;

    return (
        <div style={{ maxWidth: "600px", margin: "0 auto" }}>
            <button onClick={() => navigate("/")}>ホームに戻る</button>

            <h1>{project.name}</h1>
            <p>{project.description}</p>

            <h2>タスク一覧</h2>

            <ul>
                {tasks.map((t) => (
                    <li key={t.id} style={{ marginBottom: "8px" }}>
                        {editingTaskId === t.id ? (
                            <div>
                                <input
                                    value={editTitle}
                                    onChange={(e) => setEditTitle(e.target.value)}
                                    style={{ marginRight: "4px" }}
                                />
                                <input
                                    value={editStatus}
                                    onChange={(e) => setEditStatus(e.target.value)}
                                    style={{ marginRight: "4px" }}
                                    placeholder="status"
                                />
                                <input
                                    type="number"
                                    value={editPriority}
                                    onChange={(e) => setEditPriority(Number(e.target.value))}
                                    style={{ width: "60px", marginRight: "4px" }}
                                />
                                <button onClick={saveEdit}>保存</button>
                                <button onClick={cancelEditing}>キャンセル</button>
                            </div>
                        ) : (
                            <div>
                                {t.title} - {t.status} - 優先度: {t.priority}
                                <button
                                    style={{ marginLeft: "8px" }}
                                    onClick={() => startEditing(t)}
                                >
                                    編集
                                </button>
                                <button
                                    style={{ marginLeft: "4px", color: "red" }}
                                    onClick={() => handleDeleteTask(t.id)}
                                >
                                    削除
                                </button>
                            </div>
                        )}
                    </li>
                ))}
            </ul>

            {/* 新規タスク作成フォーム */}
            <form onSubmit={handleAddTask}>
                <input
                    type="text"
                    placeholder="新規タスク名"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    required
                    style={{ marginRight: "8px" }}
                />
                <button type="submit">追加</button>
            </form>
        </div>
    );
}

export default Project;