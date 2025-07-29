import { useState } from "react";
import "./index.css";
import { useNavigate } from "react-router-dom";
import postApi from "../../services/apis/postApi";
import HEADER from "../../constant/header";
import useMediaQuery from "@mui/material/useMediaQuery";
import DesktopLayout from "../../component/DesktopLayout/DeskTopLayout";

export default function ReportPage() {
  const isMobile = useMediaQuery('(max-width:1100px)');
  const navigate = useNavigate();

  const [imageFiles, setImageFiles] = useState([]);
  const [detail, setDetail] = useState("");

  const [image, setImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
    }
  };

  const handleFileChange = (e) => {
    const files = e.target.files;
    setImageFiles(files);
  };

  const onDetailChange = (e) => {
    setDetail(e.target.value);
  };

  const postReport = async () => {
    const formData = new FormData();
    if (imageFiles) {
      for (let file of imageFiles) {
        formData.append("images", file); // "images" 키로 여러 파일 추가
      }
    }

    const send_data = {
      header: HEADER,
      body: {
        detail: detail,
      },
    };

    const config = {
      headers: {
        "Content-Type": "multipart/form-data", // 반드시 설정
      },
    };

    formData.append("jsonData", JSON.stringify(send_data));

    await postApi.post("nova_sub_system/try_report_bug", formData, config).then((res) => {
      if (res.data.body.result) {
        alert("전송 완료");
      }
    });
  };

  if (isMobile){
    return (
      <div className="container ReportPage">
        <div className="ReportPage_title">
          <button
            onClick={() => {
              navigate(-1);
            }}
          >
            돌아가기
          </button>
          <div>버그 리포트</div>
        </div>

        <div className="Report_notice">
          <p>
            불편을 드려 죄송합니다.
            <br />
            발생한 문제를 신속하게 해결하기 위해 귀하의 도움이 필요합니다. <br />
            버그에 대한 자세한 설명과 함께 어떻게 발생했는지에 대한 정보를 제공해 주시면 더욱 신속하고
            정확한 조치를 취할 수 있습니다.
            <br />
            감사합니다.
          </p>
        </div>

        <div className="Report_notice">
          <div className="Report_image">
            <div className="img_box">
              <img src={image} />
            </div>
            <label htmlFor="image" className="file_button">
              이미지 첨부
            </label>
            <input
              id="image"
              type="file"
              multiple
              accept="image/*"
              name="image"
              onChange={(e) => {
                handleImageChange(e);
                handleFileChange(e);
              }}
            />
          </div>
          <textarea
            className="Report_input"
            placeholder="어떤 버그를 만나셨나요?"
            onChange={(e) => {
              onDetailChange(e);
            }}
          />
        </div>

        <div className="Report_button_container">
          <button className="Report_button" onClick={postReport}>
            리포트
          </button>
        </div>
      </div>
    );
  }else{
    <DesktopLayout>
      <div className="container ReportPage">
        <div className="ReportPage_title">
          <button
            onClick={() => {
              navigate(-1);
            }}
          >
            돌아가기
          </button>
          <div>버그 리포트</div>
        </div>

        <div className="Report_notice">
          <p>
            불편을 드려 죄송합니다.
            <br />
            발생한 문제를 신속하게 해결하기 위해 귀하의 도움이 필요합니다. <br />
            버그에 대한 자세한 설명과 함께 어떻게 발생했는지에 대한 정보를 제공해 주시면 더욱 신속하고
            정확한 조치를 취할 수 있습니다.
            <br />
            감사합니다.
          </p>
        </div>

        <div className="Report_notice">
          <div className="Report_image">
            <div className="img_box">
              <img src={image} />
            </div>
            <label htmlFor="image" className="file_button">
              이미지 첨부
            </label>
            <input
              id="image"
              type="file"
              multiple
              accept="image/*"
              name="image"
              onChange={(e) => {
                handleImageChange(e);
                handleFileChange(e);
              }}
            />
          </div>
          <textarea
            className="Report_input"
            placeholder="어떤 버그를 만나셨나요?"
            onChange={(e) => {
              onDetailChange(e);
            }}
          />
        </div>

        <div className="Report_button_container">
          <button className="Report_button" onClick={postReport}>
            리포트
          </button>
        </div>
      </div>

    </DesktopLayout>
  }
}
