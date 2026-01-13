import { useState, useEffect } from 'react'

function App() {
  const [tasks, setTasks] = useState([])
  const [judulBaru, setJudulBaru] = useState("")

  const ambilData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/tasks")
      const data = await response.json()
      setTasks(data)
    } catch (error) {
      console.error("Gagal ambil data:", error)
    }
  }

  useEffect(() => {
    ambilData()
  }, [])

  const tambahTugas = async () => {
    if (!judulBaru) return
    await fetch("http://127.0.0.1:8000/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: judulBaru,
        description: "Dibuat dari React",
        is_completed: false
      })
    })
    setJudulBaru("")
    ambilData()
  }

  const hapusTugas = async (id) => {
    await fetch(`http://127.0.0.1:8000/tasks/${id}`, {
      method: "DELETE",
    })
    ambilData()
  }

  return (
    <div style={{ padding: "50px", fontFamily: "Arial", maxWidth: "600px", margin: "0 auto" }}>
      <h1 style={{ textAlign: "center", color: "#fff" }}>Tugas Fullstack</h1>
      
      <div style={{ display: "flex", gap: "10px", marginBottom: "30px" }}>
        <input 
          type="text" 
          value={judulBaru}
          onChange={(e) => setJudulBaru(e.target.value)}
          placeholder="Mau ngapain hari ini?"
          style={{ 
            padding: "12px", 
            flex: 1, 
            borderRadius: "8px", 
            border: "none",
            fontSize: "16px"
          }}
        />
        <button 
          onClick={tambahTugas} 
          style={{ 
            padding: "12px 25px", 
            background: "#007bff", 
            color: "white", 
            border: "none",
            borderRadius: "8px", 
            cursor: "pointer",
            fontWeight: "bold"
          }}>
          Tambah
        </button>
      </div>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {tasks.map((task) => (
          <li key={task.id} style={{ 
            background: "white", 
            color: "black", /* <--- INI PERBAIKANNYA BRO */
            boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
            marginBottom: "15px", 
            padding: "15px", 
            borderRadius: "10px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            borderLeft: task.is_completed ? "5px solid green" : "5px solid orange"
          }}>
            <span style={{ fontSize: "18px", fontWeight: "500" }}>
              {task.title}
            </span>
            
            <button 
              onClick={() => hapusTugas(task.id)}
              style={{ 
                background: "#ff4d4d", 
                color: "white", 
                border: "none", 
                padding: "8px 12px", 
                borderRadius: "6px", 
                cursor: "pointer",
                fontWeight: "bold",
                fontSize: "12px"
              }}
            >
              Hapus 🗑️
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App