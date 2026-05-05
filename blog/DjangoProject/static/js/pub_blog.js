<!--在添加js的时候，html的一些元素还没加载出来，需要先加载才添加-->
window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        },
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $("#submit-btn").click(function(event){
        //阻止按钮的默认功能，防止发送form表单
        event.preventDefault();
        let title = $("input[name='title']").val();
        let category = $("#category-select").val();
        //getHTML返回所有
        let content = editor.getHtml();
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax('/blog/pub',{
            method: 'POST',
            data: {title, category, content, csrfmiddlewaretoken},
            success: function(result){
                //前端向后端发送请求，可是不理解后端是怎么返回响应给前端的，我认为return应该只是返回给视图函数而已，可是怎么给前端拿到这个result呢
                if( result['code'] == 200 ){
                    let blog_id = result['data']['blog_id'];
                    window.location = '/blog/detail/' + String(blog_id);
                }else{
                    alter(result['message']);
                }
            }
        })
    })
}