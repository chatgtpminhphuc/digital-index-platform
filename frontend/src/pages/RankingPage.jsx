import { useEffect, useState } from "react";

function RankingPage() {
  const [rankings, setRankings] = useState([]);
  const [periodId, setPeriodId] = useState(1);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/stats/ranking/?period_id=${periodId}`)
      .then(res => res.json())
      .then(data => setRankings(data))
      .catch(err => console.error("Lỗi:", err));
  }, [periodId]);

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Bảng xếp hạng theo kỳ</h1>

      <label className="block mb-2 text-sm font-medium text-gray-700">
        Nhập Period ID:
      </label>
      <input
        type="number"
        value={periodId}
        onChange={(e) => setPeriodId(e.target.value)}
        className="border p-2 rounded w-32 mb-4"
      />

      <table className="w-full border border-gray-200">
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
    </div>
  );
}

export default RankingPage;
