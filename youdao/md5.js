function func(){
     r = "" + (new Date).getTime()
     , i = r + parseInt(10 * Math.random(), 10);
     return {r,i}
}