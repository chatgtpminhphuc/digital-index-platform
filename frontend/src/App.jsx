import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

function App() {
  const [rankings, setRankings] = useState([]);
  const [periods, setPeriods] = useState([]);
  const [selectedPeriodId, setSelectedPeriodId] = useState(null);

  // Lấy danh sách kỳ
  useEffect(() => {
    fetch("http://127.0.0.1:8000/data/periods/")
      .then(res => res.json())
      .then(data => {
        setPeriods(data);
        if (data.length > 0) {
          setSelectedPeriodId(data[0].id); // chọn kỳ đầu tiên mặc định
        }
      });
  }, []);

  // Gọi dữ liệu bảng xếp hạng
  useEffect(() => {
    if (!selectedPeriodId) return;
    fetch(`http://127.0.0.1:8000/stats/ranking/?period_id=${selectedPeriodId}`)
      .then(res => res.json())
      .then(data => setRankings(data));
  }, [selectedPeriodId]);

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">📊 Bảng xếp hạng theo kỳ</h1>

      {/* Dropdown chọn kỳ */}
      <label className="block mb-2 text-sm font-medium text-gray-700">
        Chọn kỳ báo cáo:
      </label>
      <select
        className="border p-2 rounded mb-6"
        value={selectedPeriodId || ""}
        onChange={(e) => setSelectedPeriodId(Number(e.target.value))}
      >
        {periods.map((period) => (
          <option key={period.id} value={period.id}>
            {period.name} ({period.code})
          </option>
        ))}
      </select>

      {/* Bảng */}
      <table className="w-full border border-gray-200 text-sm mb-8">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 text-left border">#</th>
            <th className="p-2 text-left border">Đơn vị</th>
            <th className="p-2 text-left border">Tổng điểm</th>
          </tr>
        </thead>
        <tbody>
          {rankings.map((item, index) => (
            <tr key={index} className="border">
              <td className="p-2 border">{index + 1}</td>
              <td className="p-2 border">{item.organization}</td>
              <td className="p-2 border">{item.total_score}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Biểu đồ */}
      <h2 className="text-lg font-semibold mb-2">Biểu đồ cột</h2>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={rankings}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="organization" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="total_score" fill="#4f46e5" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;

fetch("http://127.0.0.1:8000/data/periods/")
  .then(res => res.json())
  .then(data => {
    console.log("Kỳ dữ liệu:", data); // 👈 Thêm dòng này
    console.log("Period response:", data);
    setPeriods(data);
    if (data.length > 0) {
      setSelectedPeriodId(data[0].id);
    }
  });
  
