/* eslint-disable no-console */
import axios from "axios";

//A class to handle relations with the REST API
export default class RestApi {
  constructor(restUrl) {
    this.url = restUrl; //+ "/v1/";
  }

  headers() {
    return {
      "content-type": "application/json",
      accept: "application/json"
    };
  }

  getData(apiPoint, getParams = {}) {
    let currentURL = this.url + apiPoint;
    return axios({
      method: "GET",
      url: currentURL,
      params: getParams,
      headers: this.headers()
    })
      .then(result => {
        // console.log(result);
        return result.data;
      })
      .catch(error => {
        console.log(error);
        console.log("ERROR URL: " + currentURL);
      });
  }
}
