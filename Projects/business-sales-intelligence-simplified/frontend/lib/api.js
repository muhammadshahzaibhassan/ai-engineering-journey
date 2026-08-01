const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function handle(res) {
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch (_) {}
    throw new Error(detail);
  }
  return res.json();
}

export const api = {
  base: API_BASE,

  async uploadCsv(file) {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form });
    return handle(res);
  },

  async process(sessionId) {
    const res = await fetch(`${API_BASE}/process/${sessionId}`, { method: "POST" });
    return handle(res);
  },

  async salesAnalytics(sessionId) {
    const res = await fetch(`${API_BASE}/analytics/sales/${sessionId}`);
    return handle(res);
  },

  async customerAnalytics(sessionId) {
    const res = await fetch(`${API_BASE}/analytics/customers/${sessionId}`);
    return handle(res);
  },

  async trainModel(sessionId) {
    const res = await fetch(`${API_BASE}/model/train/${sessionId}`, { method: "POST" });
    return handle(res);
  },

  async predict(sessionId, modelName, features) {
    const res = await fetch(`${API_BASE}/model/predict/${sessionId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model_name: modelName, features }),
    });
    return handle(res);
  },

  async report(sessionId) {
    const res = await fetch(`${API_BASE}/report/${sessionId}`);
    return handle(res);
  },
};
