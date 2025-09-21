import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/free-mode';
import 'swiper/css/pagination';
import { FreeMode} from 'swiper/modules';


import style from "./SelectCategoryComponent.module.css";


const SelectCategoryComponent = ({
    options, category,
    setCategory,
    }) => {

    return (
        <div className={style["bias-select-section"]}>
            <span className={style["bias-select-section-title"]}>카테고리 선택</span>
            <div className={style["bias-selection-wrapper"]} >
                <Swiper
                    slidesPerView={"auto"}
                    spaceBetween={30}
                    modules={[FreeMode]}
                >
                    <SwiperSlide 
                        style={{ width: "250px"}}
                    >
                        <NoneSelectCategoryComponent
                            selectedCategory={category}
                            handleSelectCategory={setCategory}
                        />
                    </SwiperSlide>
                    {options.map((option) => (
                        <SwiperSlide
                            key={option.category}
                            style={{ width: "250px"}}
                        >
                            <CategoryComponent
                                option={option.category}
                                selectedOption={category}
                                handleSelectCategory={setCategory}
                            />
                        </SwiperSlide>
                    ))}
                </Swiper>
            </div>
        </div>
    );
};

export default SelectCategoryComponent;

const NoneSelectCategoryComponent = ({selectedCategory, handleSelectCategory}) => {
    return(
        <div className={style["bias-component-wrapper"]}>
            <div className={style["bias-component"]} 
                onClick={()=> handleSelectCategory("선택 없음")}
                style={{ border: selectedCategory == "선택 없음" ? "2px solid #8CFF99" : "2px solid #fff" }}
            >
                    <span className={style["bias-name"]}> 선택 없음 </span>
            </div>
            {
                selectedCategory== "선택 없음" &&
                 <span className={style["bias-selected-span"]}> 선택 </span> 
            }
        </div>
    );
}


const CategoryComponent = ({
    option,
    selectedOption, handleSelectCategory
}) => {

    return(
        <div className={style["bias-component-wrapper"]}>
            <div className={style["bias-component"]}
                onClick={()=>{ handleSelectCategory(option); }}
                style={{ border: option == selectedOption? "2px solid #8CFF99" : "2px solid #fff" }}
            >
                <span className={style["bias-name"]}> {option}</span>
            </div>
            {
                selectedOption == option &&
                 <span className={style["bias-selected-span"]}> 선택 </span> 
            }
        </div>
    );
}