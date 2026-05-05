$(function (){
    function bindCaptchaBtnClick(){
            <!--#代表id-->
        $("#captcha-btn").click(function(event){
            let $this = $(this);
            let email = $("input[name='email']").val();
            if(!email){
                alert("请输入邮箱");
                return;
            }
            $this.off('click')

            //'/auth/captcha?email='和'auth/captcha?email='为什么不一样？
            $.ajax('/auth/captcha?email='+email,{
                method: 'GET',
                success: function(result){
                    if(result['codoe']==200){
                        alert('验证码发送成功')
                    }else{
                        alert(result['message'])
                    }
                },
                fail: function(error){
                    console.log(error);
                }
            })

            let countdown = 6;
            let timer = setInterval(function(){
                if(countdown<=0){
                    $this.text('获取验证码');
                    clearInterval(timer);
                    bindCaptchaBtnClick();
                }else{
                    countdown--;
                    $this.text(countdown+'s')
                }
            }, 1000);
        })
    }

    bindCaptchaBtnClick();
});