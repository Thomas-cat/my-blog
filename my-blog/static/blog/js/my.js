function a(){
var myDate = new Date();
var hours = myDate.getHours();
if (hours < 11 && hours >5)
{
$('.first-word').text("早上好");
$('.second-word').text("今天也要努力哦");
}
else if (hours < 14 && hours >=11)
{
$('.first-word').text("中午好");
$('.second-word').text("今天也要努力哦");
}

else if (hours < 18 && hours >=14)
{
$('.first-word').text("下午好");
$('.second-word').text("今天也要努力哦");
}
else if (hours < 19 && hours >=18)
{
$('.first-word').text("傍晚好");
$('.second-word').text("今天也要努力哦");
}
else if (hours < 23 && hours >=19)
{
$('.first-word').text("晚上好");
$('.second-word').text("要记得劳逸结合哦");

}
else if (hours < 5 && hours >=1)
{
$('.first-word').text("凌晨了");
$('.second-word').text("赶紧睡美容觉吧");
}
else
{
$('.first-word').text("深夜咯");
$('.second-word').text("要注意休息哦");

}

}
