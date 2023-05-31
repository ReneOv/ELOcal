import axios from "axios";
import { baseURL, headers } from "./config";

export const getAllLeagues = async (): Promise<any> => {
    const data = await axios
        .get(`${baseURL}/league/`, {headers: headers})
        .then((res) => {
            return res;
        })
        .catch((e) => {
            console.log(e);
        });
    
    return data;
};

export const getLeague = async (id: string): Promise<any> => {
    const data = await axios
        .get(`${baseURL}/league/${id}/`, {headers: headers})
        .then((res) => {
            return res;
        })
        .catch((e) => {
            console.log(e)
        });
    
    return data;
};

export const getLeagueRanking = async (id: string): Promise<any> => {
    const data = await axios
        .get(`${baseURL}/league/${id}/get_ranking/`, {headers: headers})
        .then((res) => {
            return res;
        })
        .catch((e) => {
            console.log(e)
        });
    
    return data;
};