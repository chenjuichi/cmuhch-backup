import axios from 'axios';

var myAjax = {
  async listUsers () { 
      const path = '/listUsers';
      console.log("Axios get data from user table...")
      try {
        let res = await axios.get(path);
        console.log("GET ok, total records:", res.data.outputs.length);        
        this.desserts = Object.assign([], res.data.outputs);
      } catch (err) {
        console.error(err)
      }
  },  
}

export default myAjax
