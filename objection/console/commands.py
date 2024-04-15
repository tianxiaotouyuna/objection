from objection.commands import http
from ..commands import command_history
from ..commands import custom
from ..commands import device
from ..commands import filemanager
from ..commands import frida_commands
from ..commands import jobs
from ..commands import memory
from ..commands import plugin_manager
from ..commands import sqlite
from ..commands import ui
from ..commands.android import clipboard
from ..commands.android import command
from ..commands.android import general
from ..commands.android import generate as android_generate
from ..commands.android import heap as android_heap
from ..commands.android import hooking as android_hooking
from ..commands.android import intents
from ..commands.android import keystore
from ..commands.android import pinning as android_pinning
from ..commands.android import proxy as android_proxy
from ..commands.android import root
from ..commands.ios import binary
from ..commands.ios import bundles
from ..commands.ios import cookies
from ..commands.ios import generate as ios_generate
from ..commands.ios import heap as ios_heap
from ..commands.ios import hooking as ios_hooking
from ..commands.ios import jailbreak
from ..commands.ios import keychain
from ..commands.ios import monitor as ios_crypto
from ..commands.ios import nsurlcredentialstorage
from ..commands.ios import nsuserdefaults
from ..commands.ios import pasteboard
from ..commands.ios import pinning as ios_pinning
from ..commands.ios import plist
from ..utils.helpers import list_current_jobs

# commands are defined with their name being the key, then optionally
# have a meta, dynamic and commands key.

# meta: A small one-liner containing information about the command itself
# dynamic: A method to execute that would return completions to populate in the prompt
# exec: The *actual* method to execute when the command is issued.

# commands help is stored in the help files directory as a txt file.

COMMANDS = {

    'plugin': {
        'meta': '管理插件',
        'commands': {
            'load': {
                'meta': '加载插件',
                'exec': plugin_manager.load_plugin
            }
        }
    },

    '!': {
        'meta': '执行操作系统命令',
        'exec': None,  # handled in the Repl class itself
    },

    'reconnect': {
        'meta': '重新连接当前设备',
        'exec': None,  # handled in the Repl class itself
    },

    'resume': {
        'meta': '恢复附加的进程',
        'exec': None
    },

    'import': {
        'meta': '从完整路径导入 fridascript 并运行它',
        'exec': frida_commands.load_background
    },

    'ping': {
        'meta': 'ping 注入的代理',
        'exec': frida_commands.ping
    },

    # 文件管理器命令

    'cd': {
        'meta': '更改当前工作目录',
        'dynamic': filemanager.list_folders_in_current_fm_directory,
        'exec': filemanager.cd
    },

    'commands': {
        'meta': '管理当前会话中运行的命令',
        'commands': {
            'history': {
                'meta': '列出当前会话中运行的所有唯一命令',
                'exec': command_history.history,
            },
            'save': {
                'meta': '将当前会话中运行的所有唯一命令保存到文件中',
                'exec': command_history.save
            },
            'clear': {
                'meta': '清除当前会话的命令历史记录',
                'exec': command_history.clear
            }
        }
    },

    'ls': {
        'meta': '列出当前工作目录中的文件',
        'dynamic': filemanager.list_folders_in_current_fm_directory,
        'exec': filemanager.ls,
    },

    'pwd': {
        'meta': '打印设备上的当前工作目录',
        'exec': filemanager.pwd_print,
    },

    'file': {
        'meta': '管理远程文件系统上的文件',
        'commands': {
            'cat': {
                'meta': '打印文件的内容',
                'dynamic': filemanager.list_files_in_current_fm_directory,
                'exec': filemanager.cat
            },
            'upload': {
                'meta': '上传文件',
                'exec': filemanager.upload
            },
            'download': {
                'meta': '下载文件',
                'dynamic': filemanager.list_files_in_current_fm_directory,
                'exec': filemanager.download
            },

            # http 文件服务器

            'http': {
                'meta': '管理设备上的 http 文件服务器',
                'commands': {
                    'start': {
                        'meta': '在当前工作目录启动 http 服务器',
                        'exec': http.start
                    },
                    'status': {
                        'meta': '获取 http 服务器的状态',
                        'exec': http.status
                    },
                    'stop': {
                        'meta': '停止运行的 http 服务器',
                        'exec': http.stop
                    }
                }
            },
        }
    },

    'rm': {
        'meta': '删除远程文件系统中的文件',
        'dynamic': filemanager.list_files_in_current_fm_directory,
        'exec': filemanager.rm
    },

    # 设备和环境信息命令

    'env': {
        'meta': '打印有关环境的信息',
        'exec': device.get_environment
    },

    'frida': {
        'meta': '获取有关 Frida 环境的信息',
        'exec': frida_commands.frida_environment
    },

    'evaluate': {
        'meta': '在代理中评估 JavaScript',
        'exec': custom.evaluate
    },

    # 内存命令

    'memory': {
        'meta': '管理当前进程的内存',
        'commands': {
            'dump': {
                'meta': '转储进程内存的各个部分',
                'commands': {
                    'all': {
                        'meta': '转储整个当前进程的内存',
                        'exec': memory.dump_all
                    },

                    'from_base': {
                        'meta': '从基础地址转储 (x) 字节的内存到文件',
                        'exec': memory.dump_from_base
                    }
                },
            },

            'list': {
                'meta': '列出与当前进程相关的内存信息',
                'commands': {
                    'modules': {
                        'meta': '列出当前进程加载的模块',
                        'flags': ['--json'],
                        'exec': memory.list_modules
                    },

                    'exports': {
                        'meta': '列出模块的导出',
                        'flags': ['--json'],
                        'exec': memory.list_exports
                    }
                },
            },

            'search': {
                'meta': '在应用程序内存中搜索模式',
                'flags': ['--string', '--offsets-only'],
                'exec': memory.find_pattern
            },

            'write': {
                'meta': '将原始字节写入内存地址。请谨慎使用！',
                'flags': ['--string'],
                'exec': memory.write
            }
        },
    },

    # sqlite 命令

    'sqlite': {
        'meta': '管理 SQLite 数据库',
        'commands': {
            'connect': {
                'meta': '连接到 SQLite 数据库文件',
                'flags': ['--sync'],
                'dynamic': filemanager.list_files_in_current_fm_directory,
                'exec': sqlite.connect
            }
        }
    },

    # 作业命令

    'jobs': {
        'meta': '管理 objection 作业',
        'commands': {
            'list': {
                'meta': '列出所有当前作业',
                'exec': jobs.show
            },
            'kill': {
                'meta': '终止作业。这将卸载脚本',
                'dynamic': list_current_jobs,
                'exec': jobs.kill
            }
        }
    },

    # 通用用户界面命令

    'ui': {
        'meta': '通用用户界面命令',
        'commands': {
            'alert': {
                'meta': '显示警报消息，可选地指定要显示的消息。 (目前会使 iOS 崩溃)',
                'exec': ui.alert
            }
        }
    },
    # android commands

    'android': {
        'meta': 'Android 相关命令',
        'commands': {
            'deoptimize': {
                'meta': '强制虚拟机在解释器中执行所有代码',
                'exec': general.deoptimise
            },
            'shell_exec': {
                'meta': '执行 shell 命令',
                'exec': command.execute
            },
            'hooking': {
                'meta': '用于在 Android 上挂钩方法的命令',
                'commands': {
                    'list': {
                        'meta': '列出各种信息',
                        'commands': {
                            'classes': {
                                'meta': '列出当前加载的类',
                                'exec': android_hooking.show_android_classes
                            },
                            'class_methods': {
                                'meta': '列出类上可用的方法',
                                'exec': android_hooking.show_android_class_methods
                            },
                            'class_loaders': {
                                'meta': '列出已注册的类加载器',
                                'exec': android_hooking.show_android_class_loaders
                            },
                            'activities': {
                                'meta': '列出已注册的 activities',
                                'exec': android_hooking.show_registered_activities
                            },
                            'receivers': {
                                'meta': '列出已注册的 BroadcastReceivers',
                                'exec': android_hooking.show_registered_broadcast_receivers
                            },
                            'services': {
                                'meta': '列出已注册的 Services',
                                'exec': android_hooking.show_registered_services
                            },
                        }
                    },
                    'watch': {
                        'meta': '监听 Android Java 调用',
                        'exec': android_hooking.watch,
                        'flags': ['--dump-args', '--dump-backtrace', '--dump-return']
                    },
                    'set': {
                        'meta': '设置各种值',
                        'commands': {
                            'return_value': {
                                'meta': '设置方法的返回值。仅支持布尔返回值。',
                                'exec': android_hooking.set_method_return_value,
                                'flags': ['--dump-args', '--dump-return', '--dump-backtrace']
                            }
                        }
                    },
                    'get': {
                        'meta': '获取各种值',
                        'commands': {
                            'current_activity': {
                                'meta': '获取当前前台 activity',
                                'exec': android_hooking.get_current_activity
                            }
                        }
                    },
                    'search': {
                        'meta': '搜索各类类和方法',
                        'exec': android_hooking.search,
                        'flags': ['--json', '--only-classes']
                    },
                    'notify': {
                        'meta': '当类可用时通知',
                        'exec': android_hooking.notify
                    },
                    'generate': {
                        'meta': '为 Android 生成 Frida 钩子',
                        'commands': {
                            'class': {
                                'meta': '通用类钩子管理器',
                                'exec': android_generate.clazz
                            },
                            'simple': {
                                'meta': '为每个类方法生成简单钩子',
                                'exec': android_generate.simple
                            }
                        }
                    }
                },
            },
            'heap': {
                'meta': '用于操作 Android 堆的命令',
                'commands': {
                    'search': {
                        'meta': '搜索当前 Android 堆中的信息',
                        'commands': {
                            'instances': {
                                'meta': '搜索特定类的实例',
                                'exec': android_heap.instances

                            }
                        }
                    },
                    'print': {
                        'meta': '打印 Android 堆上对象的信息',
                        'commands': {
                            'fields': {
                                'meta': '打印 Java 对象实例字段',
                                'exec': android_heap.fields
                            },
                            'methods': {
                                'meta': '打印 Android 句柄的实例方法',
                                'flags': ['--without-arguments'],
                                'exec': android_heap.methods
                            }
                        }
                    },
                    'execute': {
                        'meta': '在 Java 类句柄上执行方法',
                        'flags': ['--return-string'],
                        'exec': android_heap.execute
                    },
                    'evaluate': {
                        'meta': '在 Java 类句柄上执行 JavaScript',
                        'exec': android_heap.evaluate
                    }
                }
            },
            'keystore': {
                'meta': '用于操作 Android KeyStore 的命令',
                'commands': {
                    'list': {
                        'meta': '列出 Android KeyStore 中的条目',
                        'exec': keystore.entries
                    },
                    'detail': {
                        'meta': '列出 Android KeyStore 中的所有条目详细信息',
                        'flags': ['--json'],
                        'exec': keystore.detail
                    },
                    'clear': {
                        'meta': '清除 Android KeyStore',
                        'exec': keystore.clear
                    },
                    'watch': {
                        'meta': '监听 Android KeyStore 的使用情况',
                        'exec': keystore.watch
                    }
                }
            },
            'clipboard': {
                'meta': '用于操作 Android 剪贴板的命令',
                'commands': {
                    'monitor': {
                        'meta': '监听 Android 剪贴板',
                        'exec': clipboard.monitor
                    }
                }
            },
            'intent': {
                'meta': '用于操作 Android intent 的命令',
                'commands': {
                    'launch_activity': {
                        'meta': '使用 intent 启动 Activity 类',
                        'exec': intents.launch_activity
                    },
                    'launch_service': {
                        'meta': '使用 intent 启动 Service 类',
                        'exec': intents.launch_service
                    }
                }
            },
            'root': {
                'meta': '用于操作 Android root 检测的命令',
                'commands': {
                    'disable': {
                        'meta': '尝试禁用 root 检测',
                        'exec': root.disable
                    },
                    'simulate': {
                        'meta': '尝试模拟 root 环境',
                        'exec': root.simulate
                    }
                }
            },
            'sslpinning': {
                'meta': '用于操作 Android SSL pinning 的命令',
                'commands': {
                    'disable': {
                        'meta': '尝试禁用各种 Java 库/类中的 SSL pinning',
                        'flags': ['--quiet'],
                        'exec': android_pinning.android_disable
                    }
                }
            },
            'proxy': {
                'meta': '用于为应用程序设置代理的命令',
                'commands': {
                    'set': {
                        'meta': '为应用程序设置代理',
                        'exec': android_proxy.android_proxy_set
                    }
                }
            },
            'ui': {
                'meta': 'Android 用户界面命令',
                'commands': {
                    'screenshot': {
                        'meta': '对当前 Activity 进行截图',
                        'exec': ui.android_screenshot
                    },
                    'FLAG_SECURE': {
                        'meta': '控制当前 Activity 的 FLAG_SECURE 标志',
                        'exec': ui.android_flag_secure
                    },
                }
            },
        },
    },

    # ios commands
    'ios': {
        'meta': 'iOS 相关的命令',
        'commands': {
            'info': {
                'meta': '获取 iOS 和应用程序相关的信息',
                'commands': {
                    'binary': {
                        'meta': '获取应用程序二进制和动态库的信息',
                        'exec': 'binary.info'
                    }
                }
            },
            'keychain': {
                'meta': '使用 iOS 钥匙串',
                'commands': {
                    'dump': {
                        'meta': '为当前应用的授权组转储钥匙串',
                        'flags': ['--json', '--smart'],
                        'exec': 'keychain.dump'
                    },
                    'dump_raw': {
                        'meta': '转储原始的、未处理的钥匙串条目（高级）',
                        'exec': 'keychain.dump_raw'
                    },
                    'clear': {
                        'meta': '删除当前应用的授权组的所有钥匙串条目',
                        'exec': 'keychain.clear'
                    },
                    'add': {
                        'meta': '向 iOS 钥匙串添加条目',
                        'flags': ['--account', '--service', '--data'],
                        'exec': 'keychain.add'
                    }
                }
            },
            'plist': {
                'meta': '使用 iOS Plist',
                'commands': {
                    'cat': {
                        'meta': '猫一个 Plist',
                        'dynamic': 'filemanager.list_files_in_current_fm_directory',
                        'exec': 'plist.cat'
                    }
                }
            },
            'bundles': {
                'meta': '使用 iOS 包',
                'commands': {
                    'list_frameworks': {
                        'meta': '列出应用程序的所有代表框架的包',
                        'flags': ['--include-apple-frameworks', '--full-path'],
                        'exec': 'bundles.show_frameworks'
                    },
                    'list_bundles': {
                        'meta': '列出应用程序的所有非框架包',
                        'flags': ['--full-path'],
                        'exec': 'bundles.show_bundles'
                    }
                }
            },
            'nsuserdefaults': {
                'meta': '使用 NSUserDefaults',
                'commands': {
                    'get': {
                        'meta': '获取所有条目',
                        'exec': 'nsuserdefaults.get'
                    }
                }
            },
            'nsurlcredentialstorage': {
                'meta': '使用共享的 NSURLCredentialStorage',
                'commands': {
                    'dump': {
                        'meta': '转储共享的 NSURLCredentialStorage 中的所有凭证',
                        'exec': 'nsurlcredentialstorage.dump'
                    }
                }
            },
            'cookies': {
                'meta': '使用共享的 cookie',
                'commands': {
                    'get': {
                        'meta': '获取当前应用的共享 cookie',
                        'flags': ['--json'],
                        'exec': 'cookies.get'
                    }
                }
            },
            'ui': {
                'meta': 'iOS 用户界面命令',
                'commands': {
                    'alert': {
                        'meta': ('显示一个警报消息，可选择显示特定的消息。（目前会使 iOS 崩溃）'),
                        'exec': 'ui.alert'
                    },
                    'dump': {
                        'meta': '转储序列化的 UI',
                        'exec': 'ui.dump_ios_ui'
                    },
                    'creenshot': {
                        'meta': '截取当前 UIView 的屏幕截图',
                        'exec': 'ui.ios_screenshot'
                    },
                    'biometrics_bypass': {
                        'meta': '钩住 iOS 生物识别 LAContext 并响应成功的身份验证',
                        'exec': 'ui.bypass_touchid'
                    }
                }
            },
            'heap': {
                'meta': '用于操作 iOS 堆的命令',
                'commands': {
                    'print': {
                        'meta': '打印有关 iOS 堆上对象的信息',
                        'commands': {
                            'ivars': {
                                'meta': '打印 Objective-C 对象的实例变量',
                                'flags': ['--to-utf8'],
                                'exec': 'ios_heap.ivars'
                            },
                            'methods': {
                                'meta': '打印 Objective-C 对象的实例方法',
                                'flags': ['--without-arguments'],
                                'exec': 'ios_heap.methods'
                            }
                        }
                    },
                    'search': {
                        'meta': '搜索当前 iOS 堆上的信息',
                        'commands': {
                            'instances': {
                                'meta': '搜索特定类的活动实例',
                                'exec': 'ios_heap.instances'
                            }
                        }
                    },
                    'execute': {
                        'meta': '在 iOS 堆上的对象上执行方法',
                        'flags': ['--return-string'],
                        'exec': 'ios_heap.execute'
                    },
                    'evaluate': {
                        'meta': '在 iOS 堆上的对象上评估 JavaScript',
                        'flags': ['--inline'],
                        'exec': 'ios_heap.evaluate'
                    }
                }
            },
            'hooking': {
                'meta': '用于在 iOS 中挂钩方法的命令',
                'commands': {
                    'list': {
                        'meta': '列出各种信息',
                        'commands': {
                            'classes': {
                                'meta': '列出当前应用中的类',
                                'exec': 'ios_hooking.show_ios_classes'
                            },
                            'class_methods': {
                                'meta': '列出类中的方法',
                                'flags': ['--include-parents'],
                                'exec': 'ios_hooking.show_ios_class_methods'
                            }
                        }
                    },
                    'watch': {
                        'meta': '监视类和方法的调用',
                        'exec': 'ios_hooking.watch',
                        'flags': ['--dump-args', '--dump-backtrace', '--dump-return']
                    },
                    'et': {
                        'meta': '设置各种值',
                        'commands': {
                            'eturn_value': {
                                'meta': '设置方法的返回值。仅支持布尔返回',
                                'exec': 'ios_hooking.set_method_return_value'
                            }
                        }
                    },
                    'search': {
                        'meta': '搜索各种类和或方法',
                        'exec': 'ios_hooking.search',
                        'flags': ['--json', '--only-classes']
                    },
                    'generate': {
                        'meta': '为 iOS 生成 Frida 挂钩',
                        'commands': {
                            'class': {
                                'meta': '类的通用挂钩管理器',
                                'exec': 'ios_generate.clazz'
                            },
                            'imple': {
                                'meta': '为每个类方法的简单挂钩',
                                'exec': 'ios_generate.simple'
                            }
                        }
                    }
                }
            },
            'pasteboard': {
                'meta': '使用 iOS 剪贴板',
                'commands': {
                    'onitor': {
                        'meta': '监视 iOS 剪贴板',
                        'exec': 'pasteboard.monitor'
                    }
                }
            },
            'sslpinning': {
                'meta': '使用 iOS SSL 固定 Work with iOS SSL pinning',
                'commands': {
                    'disable': {
                        'meta': '尝试在各种情况下禁用 SSL 固定。 iOS 库/类',
                        'flags': ['--quiet'],
                        'exec': 'ios_pinning.ios_disable'
                    }
                }
            },
            'jailbreak': {
                'meta': '使用 iOS 越狱检测',
                'commands': {
                    'disable': {
                        'meta': '尝试禁用越狱检测',
                        'exec': 'jailbreak.disable'
                    },
                    'imulate': {
                        'meta': '尝试模拟越狱环境',
                        'exec': 'jailbreak.simulate'
                    },
                }
            },
            'monitor': {
                'meta': '用于操作 iOS 函数监控的命令',
                'commands': {
                    'crypto': {
                        'meta': '监控 CommonCrypto 操作',
                        'exec': 'ios_crypto.crypto_enable'
                    }
                }
            },
        }
    },

    'exit': {
        'meta': '退出',
    },
}