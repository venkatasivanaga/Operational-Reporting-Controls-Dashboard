const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export type MetricsSummary = {
  open_incidents: number;
  pass_rate: number | null;
  mttr_hours: number | null;
  incidents_by_status: Record<string, number>;
  tests_by_result: Record<string, number>;
};

export async function getMetricsSummary(): Promise<MetricsSummary> {
  const res = await fetch(${API_BASE_URL}/api/metrics/summary);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(Metrics request failed:  );
  }
  return res.json();
}
