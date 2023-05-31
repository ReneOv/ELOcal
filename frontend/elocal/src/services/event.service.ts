import axios from "axios";
import { baseURL, headers } from "./config";

export const getAllEvents = async (): Promise<any> => {
    const data = await axios
        .get(`${baseURL}/event/`, {headers: headers})
        .then((res) => {
            return res;
        })
        .catch((e) => {
            console.log(e);
        });
    
    return data;
}