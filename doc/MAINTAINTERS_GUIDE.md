Checklist những việc cần làm trước khi release một phiên bản mới:

- Triển khai những bản beta trước release, ít nhất phải thông báo trên mailing
  list (xem bên dưới).
- Bump version.
- Viết NEWS, tóm tắt những thay đổi ảnh hưởng đến người dùng; nên tìm cả trong
  git history và trong Github issue.
- Chạy `dch --increment`, list những thay đổi trong NEWS nào đấy.
- Kiểm tra lại tất cả dependency xem có gì thay đổi phải báo với package maintainer


Những việc cần làm để release bản beta:
- Bump version
- Cũng chạy `dch --increment` nhưng tự sửa version thành dạng 0.2.99~beta<version>
  VD: nếu bản tiếp theo là 0.3.0 thì các bản beta sẽ là 0.2.99~beta{1,2,3}.
  Cần phải làm thế này để hệ thống quản lý package của Debian luôn xếp version của
  beta trước version của release (0.3~beta1 thường sẽ bị coi là bản mới hơn của
  0.3). Chú ý: không commit những thay đổi trong `debian/changelog` cho bản beta
  mà chỉ bản release.
- Chạy `debuild -S` để tạo signed source package.
- `dput <ppa> *-sources.dsc` để push lên build farm của Ubuntu.


Lệnh để tạo tarball:

        git archive <branch> | bzip2 > ibus-bogo_<version>.tar.bz2

Vì trong thư mục gốc đã có file `.gitattributes` nên những thứ không cần thiết
như `/debian, .gitignore` sẽ không được cho vào tarball.


Bump version: tạm thời làm bằng tay. Sửa file ibus_engine/data/bogo.xml, key
<version> và file ibus_engine/main.py:

    IBus.Component.new("org.freedesktop.IBus.BoGoPython",
                       "ibus-bogo for IBus",
                       "0.2",  # sửa ở đây
                       "GPLv3",
                       "ibus-bogo Development Team <bogoengine-dev@googlegroups.com>",
                       "https://github.com/BoGoEngine/ibus-bogo",
                       "/usr/bin/exec",
                       "ibus-bogo")
