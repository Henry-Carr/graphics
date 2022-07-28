

console.log("External JS File Connected to Index.html using script at the bottom of the page");

let cnv;

// loads the size of the canvas when the window first loads
window.onload = function(){
    console.log("loading.");
    cnv = document.getElementById("cnv");
    cnv.style.backgroundColor = "#ffffff";
    prepareDocument();
    resizeCanvas();
    drawRect();
}

// loads the size of the canvas when the window changes its size
window.onresize = function(){
    console.log("resizing.");
    drawRect();
}

//sets canvas size to the inner window size
function resizeCanvas(){
    cnv.width = window.innerWidth;
    cnv.height = window.innerHeight;
    console.log("Canvas Size: "+cnv.width+" x "+ cnv.height);
}

//removes margin and padding from window
function prepareDocument(){
    document.body.style.padding = "0px";
    document.body.style.margin = "0px";

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function formatting_from_python(){
    var values = document.getElementById("the data from python").innerHTML;
    values = JSON.parse(values);
    var python_data = [values.perimetre,values.outer_perim,values.xy_max_lens,values.perimetre_segments,values.outer_perim_segments,values.the_wall_size]
    console.log(python_data);
    return python_data
}


function roomA(roomAroom,python_data){

    if (roomAroom == 0){
        //these variables declare the sizes specified for room
        
        //var metreswidth = 10.0;
        //var metresheight = 10.0;

        var metreswidth = (python_data[2])[0];
        var metresheight = (python_data[2])[1];
        var metrewall = 1.5;
        var screenpercent = 0.75;
        var roomAspec = [metreswidth,metresheight,metrewall,screenpercent];
        return roomAspec;
    }

    if (roomAroom[0] == 1){
        
        //roomAroom = [1,metreswidth,metresheight];
        //these are the variables that declare the features
        var numberoffeatures    =   2;
        var metreslongft        =   [6,   1.5     ];
        var metreswideftA       =   [1,   0.5     ];
        var metreswideftB       =   [1,   0.5     ];
        var metresoffsetft      =   [1,   3       ];
        

        /*these are the variables that declare the where and the how the triangle features are
        var metretriangleA = [false,0,0];
        var metretriangleB = [false,0,0];
        var metretriangleC = [false,0,0];
        var metretriangleD = [false,0,0];
        */
       
        var n = 0;
        // need to add feature to stop metreslongft, metreswideftA and metreswideftB exceeding their limits
        while (n <= numberoffeatures){
            if (metreswideftA[n] > roomAroom[1]){
                metreswideftA[n] = metreswideftA[n]-(metreswideftA[n]-roomAroom[1]);
            }
            if (metreswideftB[n] > roomAroom[1]){
                metreswideftB[n] = metreswideftB[n]-(metreswideftB[n]-roomAroom[1]);
            }
            n = n + 1;
        }

        if (metreswideftA[0] > metreswideftB[0]){
            var metreshyp = Math.sqrt((metreswidth**2) + ((metreswideftA[0]-metreswideftB[0])**2));
            var ang = Math.atan(metreslongft/(metreswideftA[0]-metreswideftB[0]));
        }
        if (metreswideftA[0] < metreswideftB[0]){
            var metreshyp = Math.sqrt((metreswidth**2) + ((metreswideftB[0]-metreswideftA[0])**2));
            var ang = Math.atan(metreslongft/(metreswideftB[0]-metreswideftA[0]));
        }
        
        var roomAspec = [numberoffeatures,metreslongft,metreswideftA,metreswideftB,metreshyp,ang,metresoffsetft];
        
        var roomAspec = [1,2,3,4,5,6,7];
        return roomAspec;
    }
}

function trianglecorners(metretriangleA,metretriangleB,metretriangleC,metretriangleD,aspectratio,c){
    if (metretriangleA[0] == true){
        var pixelAX = aspectratio*metretriangleA[1]
        var pixelAY = aspectratio*metretriangleA[2]
        var hypA = Math.sqrt((pixelAX**2) + (pixelAY**2))
        var angA = ((0.0*Math.PI)-(Math.atan(pixelAY/pixelAX)));

        c.translate(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)-(pixelheight/2)+(pixelAY)));
        c.rotate(angA);
        c.beginPath();
        c.fillStyle = "#000000";
        c.rect((0),(-1*pixelwall),hypA,pixelwall);
        c.fill();
        c.closePath();
        
        var n = Math.sqrt(((hypA/2)**2)-pixelAX);
        c.beginPath();
        c.fillStyle = "#ffffff";
        c.rect((0-pixelwall),(-1*pixelwall)-(n+pixelwall),hypA+pixelwall*2,n+pixelwall);
        c.fill();
        c.closePath();

        c.rotate(-1*angA);
        c.translate(-1*((cnv.width/2)-(pixelwidth/2)),-1*((cnv.height/2)-(pixelheight/2)+(pixelAY)));
    }
    if (metretriangleB[0] == true){
        var pixelBX = aspectratio*metretriangleB[1]
        var pixelBY = aspectratio*metretriangleB[2]
        var hypB = Math.sqrt((pixelBX**2) + (pixelBY**2))
        var angB = ((0.5*Math.PI)-(Math.atan(pixelBX/pixelBY)));
        
        c.translate(((cnv.width/2)+(pixelwidth/2)),((cnv.height/2)-(pixelheight/2)+(pixelBY)));
        c.rotate(angB);
        c.beginPath();
        c.fillStyle = "#000000";
        c.rect((0)-hypB,(0)-pixelwall,hypB,pixelwall);
        c.fill();
        c.closePath();
        
        var n = Math.sqrt(((hypB/2)**2)-pixelBX);
        c.beginPath();
        c.fillStyle = "#ffffff";
        c.rect((0-pixelwall)-hypB,(0-n-pixelwall)-pixelwall,hypB+pixelwall*2,n+pixelwall);
        c.fill();
        c.closePath();

        c.rotate(-1*angB);
        c.translate(-1*((cnv.width/2)+(pixelwidth/2)),-1*((cnv.height/2)-(pixelheight/2)+(pixelBY)));
    }
    if (metretriangleC[0] == true){
        var pixelCX = aspectratio*metretriangleC[1]
        var pixelCY = aspectratio*metretriangleC[2]
        var hypC = Math.sqrt((pixelCX**2) + (pixelCY**2))
        var angC = ((0*Math.PI)-(Math.atan(pixelCY/pixelCX)));
        
        c.translate(((cnv.width/2)+(pixelwidth/2)),((cnv.height/2)+(pixelheight/2)-(pixelCY)));
        c.rotate(angC);
        c.beginPath();
        c.fillStyle = "#000000";
        c.rect((0)-hypC,(0)-0*pixelwall,hypC,pixelwall);
        c.fill();
        c.closePath();
        
        var n = Math.sqrt(((hypC/2)**2)-pixelCX);
        c.beginPath();
        c.fillStyle = "#ffffff";
        c.rect((0-pixelwall)-hypC,(0+pixelwall)-0*pixelwall,hypC+pixelwall*2,n+pixelwall);
        c.fill();
        c.closePath();

        c.rotate(-1*angC);
        c.translate(-1*((cnv.width/2)+(pixelwidth/2)),-1*((cnv.height/2)+(pixelheight/2)-(pixelCY)));
    }
    if (metretriangleD[0] == true){
        var pixelDX = aspectratio*metretriangleD[1]
        var pixelDY = aspectratio*metretriangleD[2]
        var hypD = Math.sqrt((pixelDX**2) + (pixelDY**2))
        var angD = ((0.5*Math.PI)-(Math.atan(pixelDX/pixelDY)));
        
        c.translate(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)+(pixelheight/2)-(pixelDY)));
        c.rotate(angD);
        c.beginPath();
        c.fillStyle = "#000000";
        c.rect((0),(0)-0*pixelwall,hypD,pixelwall);
        c.fill();
        c.closePath();
        
        var n = Math.sqrt(((hypD/2)**2)-pixelDX);
        c.beginPath();
        c.fillStyle = "#ffffff";
        c.rect((0-pixelwall),(0+pixelwall)-0*pixelwall,hypD+pixelwall*2,n+pixelwall);
        c.fill();
        c.closePath();

        c.rotate(-1*angD);
        c.translate(-1*((cnv.width/2)-(pixelwidth/2)),-1*((cnv.height/2)+(pixelheight/2)-(pixelDY)));
    }
}


function rectangleft(metreslongft,metresthickft,metresoffsetft,metretriangleA,metretriangleB,metretriangleC,metretriangleD,aspectratio,metreswidth,metresheight,c){
    //declares the variable to place the feature
    var pixellongft = metreslongft*aspectratio
    var pixelthickft = metresthickft*aspectratio
    var pixeloffsetft = metresoffsetft*aspectratio
    var triangleAX = metretriangleA[1]*aspectratio
    var triangleAY = metretriangleA[2]*aspectratio
    var triangleBX = metretriangleB[1]*aspectratio
    var triangleBY = metretriangleB[2]*aspectratio
    var triangleCX = metretriangleC[1]*aspectratio
    var triangleCY = metretriangleC[2]*aspectratio
    var triangleDX = metretriangleD[1]*aspectratio
    var triangleDY = metretriangleD[2]*aspectratio
    var hypA = (Math.sqrt((metretriangleA[1]**2)+(metretriangleA[2]**2)))*aspectratio
    var hypB = (Math.sqrt((metretriangleB[1]**2)+(metretriangleB[2]**2)))*aspectratio
    var hypC = (Math.sqrt((metretriangleC[1]**2)+(metretriangleC[2]**2)))*aspectratio
    var hypD = (Math.sqrt((metretriangleD[1]**2)+(metretriangleD[2]**2)))*aspectratio
    var angA = ((0.0*Math.PI)-(Math.atan(triangleAY/triangleAX)));
    var angB = ((0.5*Math.PI)-(Math.atan(triangleBX/triangleBY)));
    var angC = ((0*Math.PI)-(Math.atan(triangleCY/triangleCX)));
    var angD = ((0.5*Math.PI)-(Math.atan(triangleDX/triangleDY)));
    var metresperimetre = (hypA) + (metreswidth-(metretriangleA[1]+metretriangleB[1])) + (hypB) + (metresheight-(metretriangleB[2]+metretriangleC[2])) + (hypC) + (metreswidth-(metretriangleC[1]+metretriangleD[1])) + (hypD) + (metresheight-(metretriangleD[2]+metretriangleA[2]));
    if (metresoffsetft+metreslongft >= metresperimetre){
        metresoffsetft = metresoffsetft - metresperimetre
    }

    //places the feature on the top left corner
    if ((pixeloffsetft <= 0) && (metretriangleA[0] == false)){
        if (pixeloffsetft < 0){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)-(pixelheight/2)),(pixelthickft),(pixellongft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((cnv.width/2)-(pixelwidth/2)-(pixelwall)),((cnv.height/2)-(pixelheight/2)-(pixelwall)),(pixelthickft),(pixellongft));
            c.fill();
            c.closePath();
        }
        if (pixeloffsetft == 0){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)-(pixelheight/2)),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((cnv.width/2)-(pixelwidth/2)-(pixelwall)),((cnv.height/2)-(pixelheight/2)-(pixelwall)),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
        }
    }
    //places the feature on the top wall
    if ((pixeloffsetft+triangleAX > 0) && (pixeloffsetft+pixellongft <= (pixelwidth-(triangleAX+triangleBX)))){
        c.beginPath();
        c.fillStyle = "#000000";
        c.rect(((cnv.width/2)-(pixelwidth/2)+(pixeloffsetft+triangleAX)),((cnv.height/2)-(pixelheight/2)),(pixellongft),(pixelthickft));
        c.fill();
        c.closePath();
        c.beginPath();
        c.fillStyle = "#ffffff";
        c.rect(((cnv.width/2)-(pixelwidth/2)+(pixelwall)+(pixeloffsetft+triangleAX)),((cnv.height/2)-(pixelheight/2)-(pixelwall)),(pixellongft-2*pixelwall),(pixelthickft));
        c.fill();
        c.closePath();
    }
    //places the feature on triangle B
    if ((pixeloffsetft+pixellongft > (pixelwidth-(triangleAX+triangleBX))) && (pixeloffsetft <= (pixelwidth-(triangleAX+triangleBX)+hypB))){
        c.translate(((cnv.width/2)+(pixelwidth/2)-(triangleBX)),((cnv.height/2)-(pixelheight/2)));
        c.rotate(angB);
        if (pixeloffsetft < (pixelwidth-(triangleAX+triangleBX))){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect((0),(0),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((pixelwall)),(0-(pixelwall)),(pixellongft-2*pixelwall),(pixelthickft));
            c.fill();
            c.closePath();
        }
        if ((pixeloffsetft > (pixelwidth-(triangleAX+triangleBX))) && (pixeloffsetft+pixellongft <= (pixelwidth-(triangleAX+triangleBX))+hypB)){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect((pixeloffsetft-(pixelwidth-(triangleAX+triangleBX))),(0),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((pixelwall)+(pixeloffsetft-(pixelwidth-(triangleAX+triangleBX)))),(0-(pixelwall)),(pixellongft-2*pixelwall),(pixelthickft));
            c.fill();
            c.closePath();
        }
        c.rotate(-angB);
        c.translate(-((cnv.width/2)+(pixelwidth/2)-(triangleBX)),-((cnv.height/2)-(pixelheight/2)));
    }
    //places the feature on the top right corner
    if ((pixeloffsetft+pixellongft >= (pixelwidth-(triangleAX+triangleBX))) && (metretriangleB[0] == false)){
        //if (((pixeloffsetft+pixellongft >= (pixelwidth-(triangleAX+triangleBX))) || ((pixeloffsetft)-(pixelwidth-(triangleAX+triangleBX)) > (pixelwidth-(triangleAX+triangleBX)))) && (metretriangleB[0] == false)){
        if (pixeloffsetft < (pixelwidth-(triangleAX+triangleBX))){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect(((cnv.width/2)+(pixelwidth/2)-(pixellongft)),((cnv.height/2)-(pixelheight/2)),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((cnv.width/2)+(pixelwidth/2)-(pixellongft)+(pixelwall)),((cnv.height/2)-(pixelheight/2)-(pixelwall)),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
        }
        if (pixeloffsetft == (pixelwidth-(triangleAX+triangleBX))){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect(((cnv.width/2)+(pixelwidth/2)-(pixelthickft)),((cnv.height/2)-(pixelheight/2)),(pixelthickft),(pixellongft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((cnv.width/2)+(pixelwidth/2)-(pixelthickft)+(pixelwall)),((cnv.height/2)-(pixelheight/2)-(pixelwall)),(pixelthickft),(pixellongft));
            c.fill();
            c.closePath();
        }
    }
    //places the feature on the right wall
    if ((pixeloffsetft+pixellongft > (pixelwidth-(triangleAX+triangleBX)+hypB)) && (pixeloffsetft-(pixelwidth-(triangleAX+triangleBX))-(hypB)+(pixellongft) < (pixelheight-(triangleBY+triangleCX)))){
        c.translate(((cnv.width/2)+(pixelwidth/2)),((cnv.height/2)-(pixelheight/2)+triangleBY));
        c.rotate(Math.PI/2);
        if (pixeloffsetft < (pixelwidth-(triangleAX+triangleBX)+hypB)){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect((0),(0),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((pixelwall)),(0-(pixelwall)),(pixellongft-2*pixelwall),(pixelthickft));
            c.fill();
            c.closePath();
        }
        if ((pixeloffsetft >= (pixelwidth-(triangleAX+triangleBX)+hypB)) && (pixeloffsetft-(pixelwidth-(triangleAX+triangleBX))-(hypB)+(pixellongft) < (pixelheight-(triangleBY+triangleCX)))){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect((pixeloffsetft-((pixelwidth-(triangleAX+triangleBX))+hypB)),(0),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((pixelwall)+(pixeloffsetft-((pixelwidth-(triangleAX+triangleBX))+hypB))),(0-(pixelwall)),(pixellongft-2*pixelwall),(pixelthickft));
            c.fill();
            c.closePath();
        }
        c.rotate(Math.PI/-2);
        c.translate(-((cnv.width/2)+(pixelwidth/2)),-((cnv.height/2)-(pixelheight/2)+triangleBY));
    }
    //places the feature on the bottom right corner
    if (((pixeloffsetft-pixelwidth >= pixelheight-pixellongft) || (pixeloffsetft-(pixelwidth+pixelheight) > pixelwidth+pixelheight)) && (metretriangleC[0] == false)){
        if (pixeloffsetft < pixelwidth+pixelheight){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect(((cnv.width/2)+(pixelwidth/2)-(pixelthickft)),((cnv.height/2)+(pixelheight/2)-(pixellongft)),(pixelthickft),(pixellongft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((cnv.width/2)+(pixelwidth/2)-(pixelthickft)+(pixelwall)),((cnv.height/2)+(pixelheight/2)+(pixelwall)-(pixellongft)),(pixelthickft),(pixellongft));
            c.fill();
            c.closePath();
        }
        if (pixeloffsetft == pixelwidth+pixelheight){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect(((cnv.width/2)+(pixelwidth/2)-(pixellongft)),((cnv.height/2)+(pixelheight/2)-(pixelthickft)),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((cnv.width/2)+(pixelwidth/2)-(pixellongft)+(pixelwall)),((cnv.height/2)+(pixelheight/2)+(pixelwall)-(pixelthickft)),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
        }
    }
    //places the feature on the bottom wall
    if ((pixeloffsetft > pixelwidth+pixelheight) && (pixeloffsetft-(pixelwidth+pixelheight)+pixellongft < pixelwidth)){
        c.beginPath();
        c.fillStyle = "#000000";
        c.rect(((cnv.width/2)+(pixelwidth/2)-(pixeloffsetft-(pixelwidth+pixelheight))-(pixellongft)),((cnv.height/2)+(pixelheight/2)-(pixelthickft)),(pixellongft),(pixelthickft));
        c.fill();
        c.closePath();
        c.beginPath();
        c.fillStyle = "#ffffff";
        c.rect(((cnv.width/2)+(pixelwidth/2)+(pixelwall)-(pixeloffsetft-(pixelwidth+pixelheight))-(pixellongft)),((cnv.height/2)+(pixelheight/2)+(pixelwall)-(pixelthickft)),(pixellongft-2*pixelwall),(pixelthickft));
        c.fill();
        c.closePath();
    }
    //places the feature on the bottom left corner
    if (((pixeloffsetft-(pixelwidth+pixelheight) >= pixelwidth-pixellongft) || (pixeloffsetft-(2*pixelwidth+pixelheight) > (2*pixelwidth+pixelheight))) && (metretriangleD[0] == false)){
        if (pixeloffsetft < (2*pixelwidth+pixelheight)){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)+(pixelheight/2)-(pixelthickft)),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((cnv.width/2)-(pixelwidth/2)-(pixelwall)),((cnv.height/2)+(pixelheight/2)+(pixelwall)-(pixelthickft)),(pixellongft),(pixelthickft));
            c.fill();
            c.closePath();
        }
        if (pixeloffsetft == (2*pixelwidth+pixelheight)){
            c.beginPath();
            c.fillStyle = "#000000";
            c.rect(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)+(pixelheight/2)-(pixellongft)),(pixelthickft),(pixellongft));
            c.fill();
            c.closePath();
            c.beginPath();
            c.fillStyle = "#ffffff";
            c.rect(((cnv.width/2)-(pixelwidth/2)-(pixelwall)),((cnv.height/2)+(pixelheight/2)+(pixelwall)-(pixellongft)),(pixelthickft),(pixellongft));
            c.fill();
            c.closePath();
        }
    }
    //places the feature on the left wall
    if ((pixeloffsetft-(2*pixelwidth+pixelheight) > 0) && (pixeloffsetft+pixellongft-(2*pixelwidth+pixelheight) < pixelheight)){
        c.beginPath();
        c.fillStyle = "#000000";
        c.rect(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)+(pixelheight/2)-(pixellongft)-(pixeloffsetft-(2*pixelwidth+pixelheight))),(pixelthickft),(pixellongft));
        c.fill();
        c.closePath();
        c.beginPath();
        c.fillStyle = "#ffffff";
        c.rect(((cnv.width/2)-(pixelwidth/2)-(pixelwall)),((cnv.height/2)+(pixelheight/2)-(pixellongft)+(pixelwall)-(pixeloffsetft-(2*pixelwidth+pixelheight))),(pixelthickft),(pixellongft-2*pixelwall));
        c.fill();
        c.closePath();
    }
}

function features(metreslongft,metreswideftA,metreswideftB,metreshyp,ang,metresoffsetft,pixelwidth,pixelheight,aspectratio,c){
    var pixellongft = metreslongft*aspectratio;
    var pixelwideftA = metreswideftA*aspectratio;
    var pixelwideftB = metreswideftB*aspectratio;
    var pixelhyp = metreshyp*aspectratio;
    var pixeloffsetft = metresoffsetft*aspectratio;

    c.translate(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)-(pixelheight/2)))
    //this is where the features will be drawn

    c.translate(-((cnv.width/2)-(pixelwidth/2)),-((cnv.height/2)-(pixelheight/2)))
}

function drawing_the_room(c,python_data,aspectratio,p,pixelwidth,pixelheight){
    c.translate(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)-(pixelheight/2)))
    n = 0
    while ((python_data[p].length) > n){
        if ((python_data[p].length)-1 > n){
            m = n + 1
        }
        if ((python_data[p].length)-1 == n){
            m = 0
        }
        c.beginPath();
        c.strokeStyle = "#ff0000";
        c.moveTo(((((python_data[p])[n])[0])[0]*aspectratio),((((python_data[p])[n])[0])[1]*aspectratio));
        c.lineTo(((((python_data[p])[m])[0])[0]*aspectratio),((((python_data[p])[m])[0])[1]*aspectratio));
        c.stroke();
        n = n + 1
    }
    c.closePath();
    c.translate(-((cnv.width/2)-(pixelwidth/2)),-((cnv.height/2)-(pixelheight/2)))
}




//draws rectangles to sizes specified and keeps it centered
function drawRect(){
    console.log("aaaaaa");
    let c = cnv.getContext("2d");
    
    python_data = formatting_from_python()

    cnv.width = window.innerWidth;
    cnv.height = window.innerHeight;

    var roomAroom = 0
    roomAspec = roomA(roomAroom,python_data);
    //[metreswidth,metresheight,metrewall,screenpercent]
    metreswidth = roomAspec[0]
    metresheight = roomAspec[1]
    metrewall = roomAspec[2]
    screenpercent = roomAspec[3]

    //this makes sure that the longest length is always the width
    /*
    if (metreswidth < metresheight){
        var temp = metreswidth;
        metreswidth = metresheight;
        metresheight = temp;
    }*/
    
    //these "if" statements find the shortest axis of the window
    //and make the horisontal side of the room "screenpercent" as a percentage of it
    //this is then used to work out the vertical length of the room using
    //an aspect ratio between both of the walls leaving both lengths in pixels
    //this is done to ensure that the entire room fits in the window and doesnt
    //overlap the size of the canvas

    /*
    if (cnv.width < cnv.height){
        console.log("canvas height is longer");
        pixelwidth = cnv.width*screenpercent;
        pixelheight = pixelwidth*(metreswidth/metresheight);
    }
    if (cnv.width >= cnv.height){
        console.log("canvas width is longer");
        pixelheight = cnv.height*screenpercent;
        pixelwidth = pixelheight*(metresheight/metreswidth);
    }*/

    /*    
    if (metreswidth >= metresheight){
        var pixelheight = cnv.height*screenpercent;
        var pixelwidth = pixelheight*(wdthhght[1]);
    }
    if (metresheight > metreswidth){
        var pixelwidth = cnv.width*screenpercent;
        var pixelheight = pixelwidth*(wdthhght[0]);
    }*/

    /*
    if (pixelheight >= cnv.height){
        pixelwidth = cnv.width*screenpercent;
        pixelheight = pixelwidth*(metreswidth/metresheight);
    }
    if (pixelwidth >= cnv.width){
        pixelwidth = cnv.width*screenpercent;
        pixelheight = pixelwidth*(metreswidth/metresheight);
    }*/
    //wdthhght = [(metresheight/metreswidth),(metreswidth/metresheight)]
    //wdthhght = [(metreswidth/metresheight),(metresheight/metreswidth)]


    var pixelheight = (cnv.height*screenpercent)+1;
    var pixelwidth = (cnv.width*screenpercent)+1;


    if (cnv.height*screenpercent <= pixelheight){
        var pixelheight = cnv.height*screenpercent;
        //var pixelwidth = pixelheight*(metreswidth/metresheight);
        //var pixelwidth = pixelheight*(metresheight/metreswidth);
        var pixelwidth = pixelheight*(metreswidth/metresheight);
    }
    if (cnv.width*screenpercent <= pixelwidth){
        var pixelwidth = cnv.width*screenpercent;
        //var pixelheight = pixelwidth*(metresheight/metreswidth);
        //var pixelheight = pixelwidth*(metreswidth/metresheight);
        var pixelheight = pixelwidth*(metresheight/metreswidth);
    }


    //this is then used to find a wall thickness using
    //a ratio between the wall in meters:pixels
    var aspectratio = pixelwidth/metreswidth;
    pixelwall = metrewall*(aspectratio);

    //used to check all values are correct
    console.log("windowsize width: " + cnv.width);
    console.log("windowsize height: " + cnv.height);
    console.log("pixelwidth width: " + pixelwidth);
    console.log("pixelheight height: " + pixelheight);
    console.log("pixelwall size: " + pixelwall);

    p = 3
    while (5 > p){
        drawing_the_room(c,python_data,aspectratio,p,pixelwidth,pixelheight)
        p = p + 1
    }
    
    /*
    //this draws a rectangle that is the size specified + the wall thickness
    //and fills it in black
    c.beginPath();
    c.fillStyle = "#000000";
    c.rect(((cnv.width/2)-(pixelwidth/2)-(pixelwall)),((cnv.height/2)-(pixelheight/2)-(pixelwall)),(pixelwidth+pixelwall*2),(pixelheight+pixelwall*2));
    c.fill();
    c.closePath();

    //this draws a rectangle over the top of the one above leaving the specified
    //room size as an interior and fills it in white
    c.beginPath();
    c.fillStyle = "#ffffff";
    c.rect(((cnv.width/2)-(pixelwidth/2)),((cnv.height/2)-(pixelheight/2)),(pixelwidth),(pixelheight));
    c.fill();
    c.closePath();
    c.stroke();
    */
    //this is the four corners of where the room is meant to be
    //each of them are one metre long and as thick as the walls should be
    //they are put there for reference while editing other parts
    c.beginPath();
    c.fillStyle = "#0000ff";
    c.rect((cnv.width/2)-(pixelwidth/2)-(0*aspectratio)-(0*((python_data[5])[0])*aspectratio),(cnv.height/2)-(pixelheight/2)-(0*aspectratio)-(0*((python_data[5])[0])*aspectratio),(aspectratio),(aspectratio));
    c.rect((cnv.width/2)+(pixelwidth/2)-(1*aspectratio)-(2*((python_data[5])[0])*aspectratio),(cnv.height/2)-(pixelheight/2)-(0*aspectratio)-(0*((python_data[5])[0])*aspectratio),(aspectratio),(aspectratio));
    c.rect((cnv.width/2)+(pixelwidth/2)-(1*aspectratio)-(2*((python_data[5])[0])*aspectratio),(cnv.height/2)+(pixelheight/2)-(1*aspectratio)-(2*((python_data[5])[0])*aspectratio),(aspectratio),(aspectratio));
    c.rect((cnv.width/2)-(pixelwidth/2)-(0*aspectratio)-(0*((python_data[5])[0])*aspectratio),(cnv.height/2)+(pixelheight/2)-(1*aspectratio)-(2*((python_data[5])[0])*aspectratio),(aspectratio),(aspectratio));

    /*
    c.rect((cnv.width/2)-(pixelwidth/2)-(0*aspectratio),(cnv.height/2)-(pixelheight/2)-(0*pixelwall),(aspectratio),(pixelwall));
    c.rect((cnv.width/2)+(pixelwidth/2)-(1*aspectratio),(cnv.height/2)-(pixelheight/2)-(0*pixelwall),(aspectratio),(pixelwall));
    c.rect((cnv.width/2)+(pixelwidth/2)-(1*aspectratio),(cnv.height/2)+(pixelheight/2)-(1*pixelwall),(aspectratio),(pixelwall));
    c.rect((cnv.width/2)-(pixelwidth/2)-(0*aspectratio),(cnv.height/2)+(pixelheight/2)-(1*pixelwall),(aspectratio),(pixelwall));
    */
    c.fill();
    c.closePath();


    //[numberoffeatures,metreslongft,metreswideftA,metreswideftB,metreshyp,ang,metresoffsetft];
    var roomAroom = [1,metreswidth,metresheight];
    roomAspec = roomA(roomAroom,python_data);

    numberoffeatures = roomAspec[0]
    var n = 0;
    while (n < numberoffeatures){
        metreslongft    = (roomAspec[1])[n]
        metreswideftA   = (roomAspec[2])[n]
        metreswideftB   = (roomAspec[3])[n]
        metreshyp       = (roomAspec[4])
        ang             = (roomAspec[5])
        metresoffsetft  = (roomAspec[6])[n]
        console.log("the code gets this far")
        features(metreslongft,metreswideftA,metreswideftB,metreshyp,ang,metresoffsetft,pixelwidth,pixelheight,aspectratio,c);
        //rectangleft(metreslongft,metresthickft,metresoffsetft,metretriangleA,metretriangleB,metretriangleC,metretriangleD,aspectratio,metreswidth,metresheight,c);
        n = n + 1
    }












    var metreslongdoor      =   0.8;
    var metresthickdoor     =   0.05;
    var pixellongdoor = metreslongdoor*aspectratio;
    var pixelthickdoor = metresthickdoor*aspectratio;
    c.beginPath();
    c.translate(((cnv.width/2)),((cnv.height/2)-(pixelwall/2)-(pixelthickdoor/2)));
    c.rotate(45 * Math.PI / 180);
    c.fillStyle = "#000000";
    c.rect(0,0,pixellongdoor,pixelthickdoor);
    c.fill();
    c.closePath();
    c.beginPath();
    c.fillStyle = "#000000";
    c.moveTo(0,(pixelthickdoor));
    c.arc(0,(pixelthickdoor),(pixellongdoor),Math.PI*(0/3),Math.PI*(1/3),false);
    c.fill();
    c.closePath();
    c.beginPath();
    c.fillStyle = "#ffffff";
    c.moveTo((pixelthickdoor/2),(pixelthickdoor));
    c.arc((pixelthickdoor/2),(pixelthickdoor),(pixellongdoor-pixelthickdoor),Math.PI*(0/3),Math.PI*(1/3),false);
    c.fill();
    c.closePath();

    c.rotate(-45 * Math.PI / 180);
    c.translate((-1*(cnv.width/2)),(-1*(cnv.height/2)+(pixelwall/2)+(pixelthickdoor/2)));
    //c.translate(0,0);
    c.beginPath();
    c.fillStyle = "#ff0000";
    c.rect((0),(0),aspectratio,aspectratio);
    //c.rect((cnv.width/2),((cnv.height/2)-(pixelwall/2)-(pixelthickdoor/2)),pixellongdoor,pixelthickdoor);
    c.fill();
    c.closePath();
}






aaaaaaaaaahhhhhhhhhhhh = drawRect()












