import React, { useEffect, useState } from 'react';

function App() {
  const [indexes, setIndexes] = useState([]);        // Danh sách bộ chỉ số
  const [periods, setPeriods] = useState([]);        // Danh sách kỳ cho bộ chỉ số đã chọn
  const [selectedIndex, setSelectedIndex] = useState('');  // ID bộ chỉ số được chọn
  const [selectedPeriod, setSelectedPeriod] = useState(''); // ID kỳ được chọn
  const [rankingData, setRankingData] = useState([]); // Dữ liệu bảng xếp hạng

  // Gọi API lấy danh sách các bộ chỉ số khi load app
  useEffect(() => {
    fetch('http://localhost:8000/periods/indexes')
      .then(res => res.ok ? res.json() : Promise.reject(res.status))
      .then(data => {
        setIndexes(data);
      })
      .catch(err => {
        console.error('Lỗi lấy danh sách bộ chỉ số:', err);
      });
  }, []);

  // Khi thay đổi bộ chỉ số được chọn
  const handleIndexChange = (e) => {
    const indexId = e.target.value;
    setSelectedIndex(indexId);
    setSelectedPeriod('');      // reset kỳ báo cáo đã chọn (nếu có)
    setRankingData([]);         // xóa dữ liệu bảng xếp hạng cũ
    if (indexId) {
      // Gọi API lấy các kỳ của bộ chỉ số được chọn
      fetch(`http://localhost:8000/periods?index_id=${indexId}`)
        .then(res => res.ok ? res.json() : Promise.reject(res.status))
        .then(data => {
          setPeriods(data);
        })
        .catch(err => {
          console.error('Lỗi lấy danh sách kỳ báo cáo:', err);
          setPeriods([]);  // trường hợp lỗi, để mảng trống
        });
    } else {
      setPeriods([]);
    }
  };

  // Khi thay đổi kỳ báo cáo được chọn
  const handlePeriodChange = (e) => {
    const periodId = e.target.value;
    setSelectedPeriod(periodId);
    if (periodId) {
      // Gọi API lấy bảng xếp hạng cho chỉ số/kỳ đã chọn
      fetch(`http://localhost:8000/stats/ranking/?period_id=${periodId}`)
        .then(res => res.ok ? res.json() : Promise.reject(res.status))
        .then(data => {
          setRankingData(data);
        })
        .catch(err => {
          console.error('Lỗi lấy dữ liệu xếp hạng:', err);
          setRankingData([]);
        });
    } else {
      setRankingData([]);
    }
  };

  return (
    <div className="App" style={{ padding: '20px' }}>
      <h2>Bảng xếp hạng theo kỳ</h2>
      {/* Dropdown chọn bộ chỉ số */}
      <label style={{ marginRight: '10px' }}>
        Chọn chỉ số:
        <select 
          value={selectedIndex} 
          onChange={handleIndexChange}
          style={{ marginLeft: '5px' }}
        >
          <option value="" disabled>-- Tất cả --</option>
          {indexes.map(idx => (
            <option key={idx.id} value={idx.id}>
              {idx.name}
            </option>
          ))}
        </select>
      </label>

      {/* Dropdown chọn kỳ báo cáo */}
      <label style={{ marginLeft: '20px', marginRight: '10px' }}>
        Kỳ báo cáo:
        <select 
          value={selectedPeriod} 
          onChange={handlePeriodChange}
          disabled={!selectedIndex}  // khóa khi chưa chọn chỉ số
          style={{ marginLeft: '5px' }}
        >
          <option value="" disabled>-- Chọn kỳ --</option>
          {periods.map(pr => (
            <option key={pr.id} value={pr.id}>
              {pr.year}
            </option>
          ))}
        </select>
      </label>

      {/* Bảng kết quả xếp hạng */}
      <table border="1" cellPadding="8" style={{ marginTop: '20px', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>#</th>
            <th>Đơn vị</th>
            <th>Tổng điểm</th>
          </tr>
        </thead>
        <tbody>
          {rankingData.length > 0 ? (
            rankingData.map((item, index) => (
              <tr key={index}>
                <td>{item.rank || index + 1}</td>
                <td>{item.unit}</td>
                <td>{item.score}</td>
              </tr>
            ))
          ) : (
            // Hiển thị thông báo hoặc dòng trống khi chưa có dữ liệu
            <tr>
              <td colSpan="3" style={{ textAlign: 'center', fontStyle: 'italic' }}>
                {selectedIndex && selectedPeriod ? 'Không có dữ liệu để hiển thị' : 'Vui lòng chọn chỉ số và kỳ báo cáo'}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default App;
