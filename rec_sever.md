# Hướng Dẫn Sử Dụng  Rec Sever
## 1.  Để recommend cho guest
- Nếu khách đang bấm xem orgs call https://recommendationsystemprojectube.herokuapp.com/events/(orgs_id)
- Nếu khách đang bấm xem events call https://recommendationsystemprojectube.herokuapp.com/orgs/(events_id)

## 2. Để recommend cho tài khoản đã đăng ký

- Nếu user đang bấm xem orgs call https://recommendationsystemprojectube.herokuapp.com/orgs/(user_id)/(orgs_id)
- Nếu user đang bấm xem events call https://recommendationsystemprojectube.herokuapp.com/events/(user_id)/(events_id)


## 3. Để recommend trang home cho guest
- call https://recommendationsystemprojectube.herokuapp.com/welcome

## 4. Để recommend trang home cho tài khoản đã đăng ký
- call https://recommendationsystemprojectube.herokuapp.com/welcome/(user_id)