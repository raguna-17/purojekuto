import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

export const register = (data) =>
    api.post("/users/", data);

export const login = (data) =>
    api.post("/users/login", data);

export const getCurrentUser = () =>
    api.get("/users/me");

export const createProject = (data) =>
    api.post("/projects/", data);

export const getProjects = () =>
    api.get("/projects/");

export const getProject = (id) =>
    api.get(`/projects/${id}`);

export const deleteProject = (id) =>
    api.delete(`/projects/${id}`);

export const createTask = (data) =>
    api.post("/tasks/", data);

export const getTasksByProject = (projectId) =>
    api.get(`/tasks/project/${projectId}`);

export const deleteTask = (id) =>
    api.delete(`/tasks/${id}`);

export default api;