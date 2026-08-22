import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export const processEmail = async (email) => {
  const response = await API.post("/emails/process", email);
  return response.data;
};

export const getDashboard = async () => {
  const response = await API.get("/dashboard");
  return response.data;
};

export const getEmails = async () => {
  const response = await API.get("/emails");
  return response.data;
};

export const getInvoices = async () => {
  const response = await API.get("/invoices");
  return response.data;
};

export const getTasks = async () => {
  const response = await API.get("/tasks");
  return response.data;
};

export const getDisputes = async () => {
  const response = await API.get("/disputes");
  return response.data;
};

export const getAuditLogs = async () => {
  const response = await API.get("/audit");
  return response.data;
};