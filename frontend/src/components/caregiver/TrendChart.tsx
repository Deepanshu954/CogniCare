"use client";

import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from "recharts";
import { CognitiveTrendPoint } from "@/types";

interface TrendChartProps {
  data: CognitiveTrendPoint[];
}

export const TrendChart: React.FC<TrendChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-slate-500 text-sm">
        No longitudinal data points available yet.
      </div>
    );
  }

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="date" stroke="#94A3B8" fontSize={12} tickLine={false} />
          <YAxis stroke="#94A3B8" fontSize={12} domain={[50, 100]} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#0F172A",
              borderColor: "#334155",
              borderRadius: "0.75rem",
              color: "#F8FAFC",
            }}
          />
          <Legend wrapperStyle={{ paddingTop: "12px", fontSize: "13px" }} />
          <Line
            type="monotone"
            dataKey="score"
            name="Session Performance Score"
            stroke="#38BDF8"
            strokeWidth={3}
            dot={{ r: 4, fill: "#38BDF8" }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="baseline_score"
            name="Personal Baseline"
            stroke="#A78BFA"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
