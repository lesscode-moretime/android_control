import flet
import uiautomator2 as u2
from flet import (Checkbox, Page, Column, ElevatedButton, Text)


def package_list_maker(dev):
    package_str = dev.shell("pm list packages -f").output
    package_full_list = package_str.split("\n")
    package_addr_list = []
    package_name_list = []

    for package_full in package_full_list:
        package_temp = package_full.split("=")
        package_name = package_temp[-1]
        del package_temp[-1]
        package_addr = "=".join(package_temp)
        package_name_list.append(package_name)
        package_addr_list.append(package_addr)

    return package_addr_list, package_name_list


def main(page: Page):
    def connect_clicked(e):
        try:
            dev = u2.connect()
            connected = True
            t.value = "휴대폰 연결에 성공하였습니다."
            page.update()
        except RuntimeError:
            connected = False
            t.value = "휴대폰 연결에 실패하였습니다. 연결 상태를 확인하고 다시 시도해주세요."
            page.update()
        if connected:
            package_list = package_list_maker(dev)
            for package in package_list:
                installed_app_view.controls.append(Checkbox(label=package[1]))

    installed_app_view = Column()

    t = Text()
    page.title = "APP Eliminator"
    page.add(installed_app_view)
    page.add(t)
    page.add(ElevatedButton(text="연결", on_click=connect_clicked))


flet.app(target=main)