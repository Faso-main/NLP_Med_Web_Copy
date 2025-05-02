import React, { useState, useRef } from 'react';
import FileDropzone from "components/FileDropzone"
import Loader from "components/Loader"
import Line from "components/Line"
import useSendPredict from "hooks/useSendPredict"

import 'css/App.css';
import "css/MainPage.css"

function App() {
  const [text, setText] = useState('');
  const { predictRequest, loading, responseData } = useSendPredict();
  const fileInputRef = useRef(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setText(reader.result);
      predictRequest({ text: reader.result });
    };
    reader.onerror = () => {
      console.error('Ошибка чтения файла', reader.error);
    };
    reader.readAsText(file, 'UTF-8');

    event.target.value = null;
  };

  const handleFileLoaded = (fileText) => {
    setText(fileText);
    predictRequest({ text: fileText });
  };

  return (
    <div className="app-container">
      <div className="title-container">
        <h1>EDSS Калькулятор</h1>
        <button onClick={handleButtonClick}>Загрузить</button>
        <input
          type="file"
          accept=".txt"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
      </div>
      {text.length !== 0 ? (
        <div className="content-container">
          <h3>Запрос:</h3>
          <p>{text}</p>

          <h3>Ответ:</h3>
          {loading ? (
            <div className="loading-container">
              <Loader />
              <p>Загрузка...</p>
            </div>
          ) : (
            <div className="response-content">
              <Line name="Итоговый EDSS" value={responseData.edss_score} isBoldName={true} />
              {Object.entries(responseData.scores).map(([k, v]) => <Line name={k} value={v} />)}
            </div>
          )}
        </div>
      ) : (
        <FileDropzone onFileLoaded={handleFileLoaded} />
      )}
    </div>
  );
}

export default App;
