# Bộ gõ tiếng Việt cho iBus

[![Build Status](https://travis-ci.org/lewtds/ibus-ringo.svg?branch=master)](https://travis-ci.org/lewtds/ibus-ringo)
[![Coverage Status](https://coveralls.io/repos/lewtds/ibus-ringo/badge.png?branch=master)](https://coveralls.io/r/lewtds/ibus-ringo?branch=master)

[*English below...*](#introduction)

**ibus-bogo** là một chương trình xử lý gõ tiếng Việt sử dụng engine **BoGo**
và được thiết kế để chạy cùng [iBus](http://code.google.com/p/ibus/),
một phần mềm quản lý các bộ gõ trong GNU/Linux.

## Cập nhật

Từ sau phiên bản 0.4, ibus-bogo sử dụng `preedit` và `surrounding text` tương tác với các ứng dụng do phương thức gửi
`fake backspace` tỏ ra không ổn định.

Phiên bản này có sự đóng góp lớn của @lewtds với *ibus-ringo*.

Để cài đặt, sau khi clone sourcecode từ github, chạy file `installer.sh`. Các gói cho các distro linux phổ biến
sẽ được phân phối trong tương lai.

Các tài liệu dưới đây đang trong quá trình sắp xếp lại. Một số tài liệu có thể đưa ra các chỉ dẫn không bắt kịp
với thực tế. Các tài liệu về API của thư viện `bogo-python` vẫn được đảm bảo.

## Hướng dẫn nhanh

1. [Cài đặt](doc/sphinx/install.rst) và sử dụng

2. Chia sẻ cho người thân

3. Trò chuyện với chúng tôi ở [mailing list của nhóm][1] hay chat qua [kênh #bogo][2] trên mạng IRC Freenode.

4. [Thông báo lỗi và đóng góp ý tưởng](https://github.com/BoGoEngine/ibus-bogo-python/issues?state=open)

5. Fork, vọc code và [tham gia phát triển cùng chúng tôi][3]!

[1]: https://groups.google.com/forum/?fromgroups#!forum/bogoengine-dev
[2]: https://kiwiirc.com/client/chat.freenode.net/?nick=bogo-user|?&theme=basic#bogo
[3]: doc/sphinx/contributing.rst

## Giấy phép sử dụng

**ibus-bogo** là
[phần mềm tự do nguồn mở](http://en.wikipedia.org/wiki/Free_and_open_source_software).

Toàn bộ mã nguồn của **ibus-bogo** và **BoGoEngine** cùng tất
cả các tài nguyên đi kèm đều được phát hành dưới các quy định ghi
trong Giấy phép Công cộng GNU, phiên bản 3.0 (GNU General Public
License v3.0).  Xem tệp [COPYING](COPYING) để biết thêm chi tiết.

## Cảm ơn

**ibus-bogo** đang được duy trì và phát triển bởi Ngô "Chin" Trung
(nick [@lewtds](https://github.com/lewtds/) trên Github).

Nhóm phát triển xin chân thành gửi lời cảm ơn đặc biệt đến:

* [Nguyễn Hà Dương](https://github.com/CMPITG)
* [Hà Quang Dương](https://github.com/haqduong)
* [Nguyễn Phan Hải](https://github.com/hainp)
* [Nguyễn Thành Hải](https://github.com/phaikawl)
* [Ngô Huy](https://github.com/NgoHuy)
* [Đàm Tiến Long](https://github.com/fuzzysource)
* [Nguyễn Đình Quân](https://github.com/Narga)
* [Duc Tran](https://github.com/sokomo) (a.k.a. kitarousa)
* [Trương Anh Tuấn](https://github.com/tuanta)


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/BoGoEngine/ibus-bogo-python/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

----

## Introduction

**ibus-bogo** is a Vietnamese input engine targeting
[IBus](http://code.google.com/p/ibus/), an input method manager in GNU/Linux
environments.

## Getting started

1. [Install](doc/sphinx/install.rst) and use just like any other IBus engine

2. Share

3. Talk to us at
   [our mailing list](https://groups.google.com/forum/?fromgroups#!forum/bogoengine-dev)
   and IRC channel at [#bogo on Freenode](https://kiwiirc.com/client/chat.freenode.net/?nick=bogo-user|?&theme=basic#bogo).

4. [Report bugs and share suggestions](https://github.com/BoGoEngine/ibus-bogo-python/issues?state=open)

5. Fork and [contribute](doc/CONTRIBUTE.md)

## License

**ibus-bogo** is [free and open source software](http://en.wikipedia.org/wiki/Free_and_open_source_software)
and is released under the GNU General Public License v3.0.

## Credits

**ibus-bogo** is actively maintained by Trung "Chin" Ngô
([@lewtds](https://github.com/lewtds/) on Github).

We would like to give thanks to:

* [Nguyễn Hà Dương](https://github.com/CMPITG)
* [Hà Quang Dương](https://github.com/haqduong)
* [Nguyễn Phan Hải](https://github.com/hainp)
* [Nguyễn Thành Hải](https://github.com/phaikawl)
* [Ngô Huy](https://github.com/NgoHuy)
* [Đàm Tiến Long](https://github.com/fuzzysource)
* [Nguyễn Đình Quân](https://github.com/Narga)
* [Duc Tran](https://github.com/sokomo) (a.k.a. kitarousa)
* [Trương Anh Tuấn](https://github.com/tuanta)

for their contributions to the project, in one way or another.
