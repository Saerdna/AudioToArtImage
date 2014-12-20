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
    sparks = $("#sparks");
    
    $.ajax({url:"../uploader", async:false, type:"post", data: {"width":sparks.width(), "height":sparks.height()}}).success(function(ret){
        arr = eval(ret);
        sparks.trigger("mousemove", [sparks.width() / 2, sparks.height() / 2]);
        sparks.trigger("mousedown", [sparks.width() / 2, sparks.height() / 2]);
        tot = 0
        console.log(arr.length);
        for(i = 0 ; i < arr.length; ++i){
            poi = [arr[i][0], arr[i][1]];
            //sparks.trigger("mousemove", poi);
            setTimeout(sleepMove(poi), tot);
            tot += 20;
        }
        setTimeout(sleepUp(), tot);
        console.log(tot);
    });
}
