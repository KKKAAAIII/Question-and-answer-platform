function bindCaptchaBtnClick(){
    // $('#element name') means get an element in the html file
    // following the # is the button id
    $('#captcha-btn').on('click', function(event){
        var email = $("input[name='email']").val();
        /*
        if(!email){
            alert('please enter email address');
            return;
        }
        */

        // send request through ajax, Async JavaScript And XML(JSON)
        // $.ajax({}) is a func provided by jquery which help you send request
        // url_for(user.captcha) can be used under the condition that it is a jinja2 template
        // in js file the format is /user/captcha
        $.ajax({
            url: '/user/captcha',
            method: 'POST',
            data:{
                'email': email
            },
            // parameter result is the result returned by view function get_captcha() in user.py
            success: function (result){
                var code = result['code'];
                if(code === 200){
                    // close click event
                    $('#captcha-btn').off('click')
                    // start count down
                    var countDown = 60;
                    //timeout unit ms, handler: this thing you want to do
                    // setInterval js built-in func, do handler after each timeout
                    var timer = setInterval(function (){
                        if(countDown > 0){
                            // rewrite the text in the button
                            $('#captcha-btn').text('resend after '+countDown+'s');
                        }else{
                            $('#captcha-btn').text('Get verification code');
                            // restore the func
                            bindCaptchaBtnClick();
                            // if no longer need timer, it is neccessary to stop it, or it will run forever
                            clearInterval(timer);
                        }
                        countDown -= 1;
                    }, 1000 );
                    alert('verification code has been sent');
                }else{
                    alert(result['message']);
                }
            }
        })
    });
}


// $ means when all elements in the web page are loaded then next execute the js code
$(function (){
   bindCaptchaBtnClick();
});