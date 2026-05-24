import "./App.css";

import { useState } from "react";

import {
  FiHome,
  FiMessageCircle,
  FiClock,
  FiSettings,
  FiX
} from "react-icons/fi";

function App() {

  // =====================================
  // STATES
  // =====================================

  const [theme, setTheme] =
    useState("dark");

  const [activePage, setActivePage] =
    useState("home");

  const [input, setInput] =
    useState("");

  const [excelFile, setExcelFile] =
    useState(null);

  const [uploadStatus, setUploadStatus] =
    useState("");

  const [uploadedFileName, setUploadedFileName] =
    useState("");

  const [showActivity, setShowActivity] =
    useState(false);

  const [showSettings, setShowSettings] =
    useState(false);

  const [showBroadcast, setShowBroadcast] =
    useState(false);

  const [broadcastType, setBroadcastType] =
    useState("whatsapp");

  const [recipients, setRecipients] =
    useState("");

  const [subject, setSubject] =
    useState("");

  const [message, setMessage] =
    useState("");

  const [activities, setActivities] =
    useState([
      "✨ Lumi initialized",
      "📄 Waiting for Excel upload"
    ]);

  // =====================================
  // QUICK ACTIONS
  // =====================================

  const actions = [

    {
      label: "🌐 Search Web",
      command: "search for "
    },

    {
      label: "💌 Send Email",
      command: "send email to "
    },

    {
      label: "💬 WhatsApp",
      command:
        "send whatsapp message to "
    },

    {
      label: "👥 Group Message",
      command:
        "send whatsapp group message to "
    },

    {
      label: "📂 Open App",
      command: "open "
    }

  ];

  // =====================================
  // SEND COMMAND
  // =====================================

  const sendCommand = async () => {

    if (!input.trim()) return;

    try {

      const response = await fetch(

        "http://127.0.0.1:8000/chat",

        {

          method: "POST",

          headers: {

            "Content-Type":
              "application/json"

          },

          body: JSON.stringify({

            text: input

          })

        }

      );

      const data =
        await response.json();

      setActivities(prev => [

        `✨ ${data.response}`,

        ...prev

      ]);

      setInput("");

    } catch (error) {

      console.log(error);

    }

  };

  // =====================================
  // UPLOAD EXCEL
  // =====================================

  const uploadExcel = async () => {

    if (!excelFile) return;

    setUploadStatus(
      "Uploading..."
    );

    const formData =
      new FormData();

    formData.append(
      "file",
      excelFile
    );

    try {

      const response = await fetch(

        "http://127.0.0.1:8000/upload-excel",

        {

          method: "POST",

          body: formData

        }

      );

      const data =
        await response.json();

      setUploadStatus(
        "✅ File uploaded successfully"
      );

      setUploadedFileName(
        excelFile.name
      );

      setActivities(prev => [

        `📄 ${data.response}`,

        ...prev

      ]);

    } catch (error) {

      console.log(error);

      setUploadStatus(
        "❌ Upload failed"
      );

    }

  };

  // =====================================
  // SMART BROADCAST
  // =====================================

  const sendSmartBroadcast =
    async () => {

      try {

        const response =
          await fetch(

            "http://127.0.0.1:8000/smart-broadcast",

            {

              method: "POST",

              headers: {

                "Content-Type":
                  "application/json"

              },

              body: JSON.stringify({

                query: recipients,

                type: broadcastType,

                subject,

                message

              })

            }

          );

        const data =
          await response.json();

        setActivities(prev => [

          `🤖 ${data.response}`,

          ...prev

        ]);

      } catch (error) {

        console.log(error);

      }

    };

  // =====================================
  // MANUAL BROADCAST
  // =====================================

  const sendManualBroadcast =
    async () => {

      try {

        const response =
          await fetch(

            "http://127.0.0.1:8000/broadcast",

            {

              method: "POST",

              headers: {

                "Content-Type":
                  "application/json"

              },

              body: JSON.stringify({

                type: broadcastType,

                recipients:
                  recipients
                    .split(",")
                    .map(item =>
                      item.trim()
                    ),

                subject,

                message

              })

            }

          );

        const data =
          await response.json();

        setActivities(prev => [

          `📢 ${data.response}`,

          ...prev

        ]);

      } catch (error) {

        console.log(error);

      }

    };

  return (

    <div className={`app ${theme}`}>

      {/* SIDEBAR */}

      <div className="sidebar">

        <div>

          <h1 className="logo">
            ✦ Lumi
          </h1>

          <p className="logo-sub">
            your cozy desktop assistant
          </p>

        </div>

        <div className="nav-links">

          <button

            className={
              activePage === "home"
                ? "active"
                : ""
            }

            onClick={() =>
              setActivePage("home")
            }

          >

            <FiHome />

            Home

          </button>

          <button

            className={
              activePage ===
              "assistant"

                ? "active"

                : ""
            }

            onClick={() =>
              setActivePage(
                "assistant"
              )
            }

          >

            <FiMessageCircle />

            Assistant

          </button>

        </div>

        <div className="bottom-icons">

          <button

            className="icon-btn"

            onClick={() =>
              setShowActivity(true)
            }

          >
            <FiClock />
          </button>

          <button

            className="icon-btn"

            onClick={() =>
              setShowSettings(true)
            }

          >
            <FiSettings />
          </button>

        </div>

      </div>

      {/* ASSISTANT PAGE */}

      {

        activePage ===
        "assistant"

        &&

        (

          <div className="assistant-page">

            <h1>
              🤖 Lumi Assistant
            </h1>

            <p>
              Your AI assistant is ready.
            </p>

            <div className="assistant-box">

              <p>
                ✨ Try commands like:
              </p>

              <ul>

                <li>
                  search for lo-fi songs
                </li>

                <li>
                  weather in kochi
                </li>

                <li>
                  open chrome
                </li>

                <li>
                  send email to xyz@gmail.com
                </li>

              </ul>

            </div>

          </div>

        )

      }

      {/* HOME PAGE */}

      {

        activePage === "home"

        &&

        (

          <div className="main-content">

            <div className="glow glow1"></div>

            <div className="glow glow2"></div>

            {/* HERO */}

            <div className="hero-section">

              <div>

                <h1 className="title">
                  Lumi ✨
                </h1>

                <p className="subtitle">
                  Your cozy automation assistant
                </p>

              </div>

              <img

                className="robot"

                src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"

                alt="robot"

              />

            </div>

            {/* COMMAND */}

            <div className="command-box">

              <input

                type="text"

                placeholder="Ask Lumi..."

                value={input}

                onChange={(e) =>
                  setInput(
                    e.target.value
                  )
                }

                onKeyDown={(e) => {

                  if (
                    e.key === "Enter"
                  ) {

                    sendCommand();

                  }

                }}

              />

              <button
                onClick={sendCommand}
              >
                Send ✨
              </button>

            </div>

            {/* ACTIONS */}

            <div className="actions">

              {

                actions.map(
                  (action, index) => (

                    <button

                      key={index}

                      className="action-pill"

                      onClick={() => {

                        setInput(
                          action.command
                        );

                      }}

                    >
                      {action.label}
                    </button>

                  )
                )

              }

              <button

                className="action-pill"

                onClick={() =>
                  setShowBroadcast(
                    true
                  )
                }

              >
                📢 Broadcast
              </button>

            </div>

            {/* EXCEL */}

            <div className="excel-section">

              <h2>
                📄 Upload Excel Sheet
              </h2>

              <input

                type="file"

                accept=".xlsx,.xls,.csv"

                onChange={(e) => {

                  setExcelFile(
                    e.target.files[0]
                  );

                }}

              />

              <button
                className="upload-btn"
                onClick={uploadExcel}
              >
                Upload Excel ✨
              </button>

              {

                uploadStatus && (

                  <div className="upload-status">

                    <p>
                      {uploadStatus}
                    </p>

                    {

                      uploadedFileName && (

                        <span>
                          📎 {uploadedFileName}
                        </span>

                      )

                    }

                  </div>

                )

              }

            </div>

            {/* TIPS */}

            <div className="tips-section">

              <h2>
                ✨ Prompt Tips
              </h2>

              <div className="tips-grid">

                <div className="tip-card">

                  <h3>
                    🌦 Weather
                  </h3>

                  <p>
                    weather in kochi
                  </p>

                </div>

                <div className="tip-card">

                  <h3>
                    💬 WhatsApp
                  </h3>

                  <p>
                    send whatsapp
                    message to amma
                  </p>

                </div>

                <div className="tip-card">

                  <h3>
                    📢 Manual Broadcast
                  </h3>

                  <p>
                    amma,Family Group
                  </p>

                </div>

                <div className="tip-card">

                  <h3>
                    🤖 Smart Excel
                  </h3>

                  <p>
                    kochi / mca / bca
                  </p>

                </div>

              </div>

            </div>

          </div>

        )

      }

      {/* ACTIVITY DRAWER */}

      {

        showActivity && (

          <div className="drawer">

            <div className="drawer-top">

              <h2>
                Recent Activity 🌙
              </h2>

              <button

                className="close-btn"

                onClick={() =>
                  setShowActivity(false)
                }

              >
                <FiX />
              </button>

            </div>

            <div className="drawer-content">

              {

                activities.map(
                  (item, index) => (

                    <div

                      key={index}

                      className="activity-item"

                    >
                      {item}
                    </div>

                  )
                )

              }

            </div>

          </div>

        )

      }

      {/* SETTINGS */}

      {

        showSettings && (

          <div className="modal-overlay">

            <div className="settings-modal">

              <div className="drawer-top">

                <h2>
                  Settings ⚙️
                </h2>

                <button

                  className="close-btn"

                  onClick={() =>
                    setShowSettings(
                      false
                    )
                  }

                >
                  <FiX />
                </button>

              </div>

              <div className="setting-card">

                <h3>
                  Theme
                </h3>

                <p>

                  Current mode:

                  {

                    theme === "dark"

                      ? " 🌙 Dark"

                      : " ☀️ Light"

                  }

                </p>

                <button

                  className="theme-toggle"

                  onClick={() => {

                    setTheme(

                      theme === "dark"

                        ? "light"

                        : "dark"

                    );

                  }}

                >
                  Switch Theme ✨
                </button>

              </div>

            </div>

          </div>

        )

      }

      {/* BROADCAST */}

      {

        showBroadcast && (

          <div className="modal-overlay">

            <div className="broadcast-modal">

              <div className="drawer-top">

                <h2>
                  📢 Broadcast Center
                </h2>

                <button

                  className="close-btn"

                  onClick={() =>
                    setShowBroadcast(
                      false
                    )
                  }

                >
                  <FiX />
                </button>

              </div>

              <div className="broadcast-tabs">

                <button

                  className={

                    broadcastType ===
                    "whatsapp"

                    ? "tab active-tab"

                    : "tab"

                  }

                  onClick={() =>
                    setBroadcastType(
                      "whatsapp"
                    )
                  }

                >
                  WhatsApp
                </button>

                <button

                  className={

                    broadcastType ===
                    "email"

                    ? "tab active-tab"

                    : "tab"

                  }

                  onClick={() =>
                    setBroadcastType(
                      "email"
                    )
                  }

                >
                  Email
                </button>

              </div>

              <input

                className="broadcast-input"

                placeholder="Recipients OR query"

                value={recipients}

                onChange={(e) =>
                  setRecipients(
                    e.target.value
                  )
                }

              />

              {

                broadcastType ===
                "email"

                &&

                (

                  <input

                    className="broadcast-input"

                    placeholder="Subject"

                    value={subject}

                    onChange={(e) =>
                      setSubject(
                        e.target.value
                      )
                    }

                  />

                )

              }

              <textarea

                className="broadcast-input message-box"

                placeholder="Type message..."

                value={message}

                onChange={(e) =>
                  setMessage(
                    e.target.value
                  )
                }

              />

              <div className="broadcast-actions">

                <button

                  className="broadcast-send"

                  onClick={
                    sendManualBroadcast
                  }

                >
                  Manual Broadcast ✨
                </button>

                <button

                  className="broadcast-send"

                  onClick={
                    sendSmartBroadcast
                  }

                >
                  Smart Excel Broadcast 🤖
                </button>

              </div>

            </div>

          </div>

        )

      }

    </div>

  );
}

export default App;