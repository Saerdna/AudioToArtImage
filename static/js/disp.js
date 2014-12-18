function move(poi){
    sparks.trigger("mousemove", poi);
}
function sleepMove(poi){
    return function()
    {
        move(poi);
    }
}
function up(){
    sparks.trigger("mouseup");
    console.log("done");
}
function sleepUp(){
    return function(){
        up();
    }
}
function flush(){
    $.ajax({url:"../uploader", async:false, type:"post"}).success(function(ret){
        arr = eval(ret);
        console.log("start");
        sparks = $("#sparks");
        console.log(sparks);
        sparks.trigger("mousemove", [402, 264]);
        sparks.trigger("mousedown", [402, 264]);
        tot = 0
        console.log(arr.length);
        for(i = 0 ; i < arr.length; ++i){
            poi = [arr[i][0], arr[i][1]];
            //sparks.trigger("mousemove", poi);
            setTimeout(sleepMove(poi), tot);
            tot += Math.random() * 20;
        }
        setTimeout(sleepUp(), tot);
        console.log(tot);
    });
}
