export const schedule = {
  sid: "1235-0agf-11tr", // schedule id
  detail: "1부 저챗, 2부 사과게임 켠왕", // schedule detail
  bid: "1008", // bias id
  bname: "허니츄러스", // bias_name
  uid: "1111-abcd-2222", // 작성자 id
  uname: "허니과메기", //작성자 이름
  start: "오후 06:00",
  end: "오후 08:00",
  date: "03월 04일",
  update_time: "3시간 전",
  location: "치지직",
  code: "ABCDEFG",
  color_code: "#FF0000",
};

export const bias = {
  bid: "1008", // bias id
  bname: "허니츄러스", // bias_name
  category: "인터넷 방송인", // bias category
  agency: "치지직", //소속
  tags: ["신입", "버츄얼", "치지직", "스트리머"],
  main_time: ["저녁", "새벽"],
  is_ad: false,
};

export const event = {
  seid: "1234-abcd-5678", // schedule event id
  sename: "플레이브 미니 3집 Caligo Pt.1 발매",
  bid: "1008",
  bname: "플레이브", // bias_name
  location: ["Yes24"],
  date: "03월 04일",
  start: "오후 06:00",
  end: "오후 08:00",
  sids: ["1235-0agf-1251", "t215-gh2h-11rc"],
  uid: "1111-abcd-2222",
  uname: "허니과메기",
};

export const schedule_bundle = {
  sbid: "121t-5t91-9ana", // schedule bundle id
  sbname: "한결 3월 1주차 방송 스케줄",
  bid: "1005",
  bname: "한결", // bias_name
  location: ["SOOP"],
  date: ["25년 03월 01일", "25년 03월 08일"],
  sids: ["1235-0agf-1251", "t215-gh2h-11rc"],
  uid: "1111-abcd-2222",
  uname: "허니과메기",
};

export const tempWeekDayData = [
  {
    date: 10,
    day: "월",
    num_schedule: 1,
  },
  {
    date: 11,
    day: "화",
    num_schedule: 2,
  },
  {
    date: 12,
    day: "수",
    num_schedule: 1,
  },
  {
    date: 13,
    day: "목",
    num_schedule: 1,
  },
  {
    date: 14,
    day: "금",
    num_schedule: 1,
  },
  {
    date: 15,
    day: "토",
    num_schedule: 1,
  },
];

export const tempScheduleData = [
  {
    timeblocks: [
      {
        time: 0,
        start: 60,
        length: 180,
      },
    ],
    schedule_detail: "저스트 채팅 짧방",
    bias_name: "도롱챠",
    color_code: "#FFC871",
  },
  {
    timeblocks: [
      {
        time: 0,
        start: 60,
        length: 300,
      },
      {
        time: 1,
        start: 0,
        length: 360,
      },
      {
        time: 2,
        start: 0,
        length: 360,
      },
    ],
    schedule_detail: "런칭 하려는 날",
    bias_name: "김민관",
    color_code: "#B171FF",
  },
  {
    timeblocks: [
      {
        time: 1,
        start: 120,
        length: 120,
      },
    ],
    schedule_detail: "사무실 가는날",
    bias_name: "잠을못자",
    color_code: "#9CF6AA",
  },
  {
    timeblocks: [
      {
        time: 0,
        start: 240,
        length: 120,
      },
      {
        time: 1,
        start: 0,
        length: 120,
      },
    ],
    schedule_detail: "원펀맨 같이보기",
    bias_name: "허니츄러스",
    color_code: "#71C4FF",
  },
  {
    timeblocks: [
      {
        time: 0,
        start: 60,
        length: 240,
      },
    ],
    schedule_detail: "원딜 연습하는 날",
    bias_name: "아리사 Arisa",
    color_code: "#71FFCD",
  },
  {
    timeblocks: [
      {
        time: 0,
        start: 300,
        length: 60,
      },
      {
        time: 1,
        start: 0,
        length: 300,
      },
    ],
    schedule_detail: "생일 특별 방송!",
    bias_name: "허니츄러스",
    color_code: "#71D9FF",
  },
  {
    timeblocks: [
      {
        time: 0,
        start: 0,
        length: 240,
      },
    ],
    schedule_detail: "행복한 합방 같은거 합니다요",
    bias_name: "다주",
    color_code: "#FFF371",
  },
];

export const mockData = [
  {
    id: 0,
    name: "한결",
    job: "인터넷 방송인",
    platform: "SOOP",
    tag: ["버추얼", "노래", "신입"],
    time: ["저녁", "새벽"],
  },
  {
    id: 1,
    name: "한결1",
    job: "인터넷 방송인",
    platform: "SOOP",
    tag: ["버추얼", "노래", "신입"],
    time: ["저녁", "새벽"],
  },
  {
    id: 2,
    name: "한결2",
    job: "인터넷 방송인",
    platform: "SOOP",
    tag: ["버추얼", "노래", "신입"],
    time: ["저녁", "새벽"],
  },
];

export const ScheduleKind = ["일정 번들", "일정", "이벤트"];

export const eventData = [
  {
    id: 0,
    name: "한결 3월 1주차 방송 스케줄",
    topic: "한결",
    date: "25년 03월 01일",
  },
  {
    id: 1,
    name: "플레이브 미니 3집",
    topic: "플레이브",
    date: "25년 03월 01일",
  },
  {
    id: 2,
    name: "한결 3월 1주차 방송 스케줄",
    topic: "한결1",
    date: "25년 03월 01일",
  },
];
