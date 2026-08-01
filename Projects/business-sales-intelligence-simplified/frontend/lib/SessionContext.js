"use client";
import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { api } from "./api";

const SessionCtx = createContext(null);
const STORAGE_KEY = "bsi_session_v1";

export function SessionProvider({ children }) {
  const [sessionId, setSessionId] = useState(null);
  const [uploadInfo, setUploadInfo] = useState(null);   // response from /upload
  const [processInfo, setProcessInfo] = useState(null); // response from /process
  const [trainInfo, setTrainInfo] = useState(null);     // response from /model/train
  const [status, setStatus] = useState("idle");         // idle | uploading | processing | ready | error
  const [error, setError] = useState(null);
  const [hydrated, setHydrated] = useState(false);

  // Restore from localStorage on first mount (browser only)
  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        setSessionId(parsed.sessionId || null);
        setUploadInfo(parsed.uploadInfo || null);
        setProcessInfo(parsed.processInfo || null);
        setTrainInfo(parsed.trainInfo || null);
        setStatus(parsed.processInfo ? "ready" : "idle");
      }
    } catch (_) {}
    setHydrated(true);
  }, []);

  // Persist whenever state changes
  useEffect(() => {
    if (!hydrated) return;
    try {
      window.localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ sessionId, uploadInfo, processInfo, trainInfo })
      );
    } catch (_) {}
  }, [hydrated, sessionId, uploadInfo, processInfo, trainInfo]);

  const uploadAndProcess = useCallback(async (file) => {
    setStatus("uploading");
    setError(null);
    try {
      const up = await api.uploadCsv(file);
      setSessionId(up.session_id);
      setUploadInfo(up);
      setStatus("processing");
      const proc = await api.process(up.session_id);
      setProcessInfo(proc);
      setTrainInfo(null);
      setStatus("ready");
      return { upload: up, process: proc };
    } catch (e) {
      setError(e.message || String(e));
      setStatus("error");
      throw e;
    }
  }, []);

  const train = useCallback(async () => {
    if (!sessionId) throw new Error("No active session -- upload a CSV first.");
    const result = await api.trainModel(sessionId);
    setTrainInfo(result);
    return result;
  }, [sessionId]);

  const reset = useCallback(() => {
    setSessionId(null);
    setUploadInfo(null);
    setProcessInfo(null);
    setTrainInfo(null);
    setStatus("idle");
    setError(null);
    try {
      window.localStorage.removeItem(STORAGE_KEY);
    } catch (_) {}
  }, []);

  const value = {
    sessionId, uploadInfo, processInfo, trainInfo, status, error, hydrated,
    uploadAndProcess, train, reset,
  };

  return <SessionCtx.Provider value={value}>{children}</SessionCtx.Provider>;
}

export function useSession() {
  const ctx = useContext(SessionCtx);
  if (!ctx) throw new Error("useSession must be used within SessionProvider");
  return ctx;
}
