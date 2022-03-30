const sidebarButton = document.querySelector('.sidebar-btn')
const sidebar = document.querySelector('.sidebar')
const dwnldBtn = document.querySelector('.dwnld')
const pageContent = document.querySelector('.page-content')
// const loginBox = document.querySelector('.login-box')
// const registerBox = document.querySelector('.register-box')

sidebarButton.addEventListener('click', () => {
    sidebar.classList.toggle('open')
    pageContent.classList.toggle('open')
    // loginBox.classList.toggle('open')
    // registerBox.classList.toggle('open')
})
dwnldBtn.addEventListener('mouseover',() => {
    dwnld = document.querySelector('.dwn-img')
    dwnld.src = '../static/img/sidebar/download/download_btn2.png'
})
dwnldBtn.addEventListener('mouseout',() => {
    dwnld = document.querySelector('.dwn-img')
    dwnld.src = '../static/img/sidebar/download/download_btn1.png'
})