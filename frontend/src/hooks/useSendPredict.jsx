import { useState } from "react";
import axios from "axios";

const apiUrl = process.env.REACT_APP_API_URL;

const useSendPredict = () => {
    const [loading, setLoading] = useState(false);
    const [responseData, setResponseData] = useState(null);
    const [error, setError] = useState(null);

    const predictRequest = async (data) => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await axios.post(`${apiUrl}/api/predict`, data, {
                headers: {
                    'Content-Type': 'application/json',
                },
                validateStatus: (status) => status < 500
            });
            
            if (response.data) {
                setResponseData(response.data);
            } else {
                setError(new Error('Пустой ответ от сервера'));
            }
        } catch (err) {
            const error = err.response?.data?.message 
                ? new Error(err.response.data.message)
                : err;
            setError(error);
            console.error('Ошибка запроса:', error);
        } finally {
            setLoading(false);
        }
    };

    const reset = () => {
        setResponseData(null);
        setError(null);
    };

    return { predictRequest, loading, responseData, error, reset };
};

export default useSendPredict;