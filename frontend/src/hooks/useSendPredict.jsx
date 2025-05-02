import { useState } from "react";
import axios from "axios";

const apiUrl = process.env.REACT_APP_API_URL;

const useSendPredict = () => {
    const [loading, setLoading] = useState(false);
    const [responseData, setResponseData] = useState(null);

    const predictRequest = async (data) => {
        setLoading(true);
        try {
            const response = await axios.post(`${apiUrl}/api/predict`, data);
            setResponseData(response.data);
        } catch (err) {
            console.log(err);
        } finally {
            setLoading(false);
        }
    };

    return { predictRequest, loading, responseData };
};

export default useSendPredict;
