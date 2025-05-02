import React, { useRef, useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import 'css/Dropzone.css';

const FileDropzone = ({ onFileLoaded }) => {
    const dropRef = useRef(null);
    const [dragActive, setDragActive] = useState(false);

    const handleFiles = useCallback(
        (files) => {
        if (!files || files.length === 0) return;
        const file = files[0];
        if (!file.name.endsWith('.txt')) return;
        const reader = new FileReader();
        reader.onload = () => onFileLoaded(reader.result);
        reader.onerror = () => console.error('Ошибка чтения файла', reader.error);
        reader.readAsText(file, 'UTF-8');
        },
        [onFileLoaded]
    );

    useEffect(() => {
        const div = dropRef.current;
        if (!div) return;

        const handleDragOver = e => {
        e.preventDefault();
        setDragActive(true);
        };
        const handleDragLeave = e => {
        e.preventDefault();
        setDragActive(false);
        };
        const handleDrop = e => {
        e.preventDefault();
        setDragActive(false);
        handleFiles(e.dataTransfer.files);
        };

        div.addEventListener('dragover', handleDragOver);
        div.addEventListener('dragleave', handleDragLeave);
        div.addEventListener('drop', handleDrop);

        return () => {
        div.removeEventListener('dragover', handleDragOver);
        div.removeEventListener('dragleave', handleDragLeave);
        div.removeEventListener('drop', handleDrop);
        };
    }, [handleFiles]);

    return (
        <div
            ref={dropRef}
            className={`dropzone ${dragActive ? 'active' : ''}`}
        >
        {dragActive ? (
            <p>Отпустите файл для загрузки</p>
        ) : (
            <div className="ddmw">
                <img src={require('assets/import.png')} alt="import"/>
                <p>Перетащите .txt файл сюда</p>
            </div>
        )}
        <input
            type="file"
            accept=".txt"
            className="dropzone-input"
            onChange={e => handleFiles(e.target.files)}
            style={{ display: 'none' }}
        />
        </div>
    );
};

FileDropzone.propTypes = {
    onFileLoaded: PropTypes.func.isRequired,
};
  
export default FileDropzone;