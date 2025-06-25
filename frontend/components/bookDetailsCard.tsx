import Image from 'next/image'
import { Rating } from 'primereact/rating'
import React from 'react'

const bookDetailsCard = ({title,author,rating,reads,desc,imgUrl}:{title:string;author:string;rating:number;reads:number;desc:string;imgUrl:string;}) => {
  return (
    <div className='max-w-[700px] bg-white shadow-2xl '>
    <div className='flex   h-full gap-8'>
      <div className='h-full flex'>
          <Image
            src={imgUrl}
            alt='book'
            width={287}
            height={435}
            className='shadow-2xl object-cover' // Add object-cover class
          />
        </div>
      <div className='flex flex-col  place-content-end w-full '>
        <h1 className='font-medium text-[38px] font-rubik pb-[15px] line-clamp-2 '>{title}</h1>
        <h1 className='text-[#626262] font-regular font-rubik pb-[10px]'>by {author}</h1>
        <Rating
          value={rating}
          cancel={false}
          readOnly
          className="text-black flex gap-1 pb-[10px]"
        />
        <h1 className='text-[#626262] font-regular font-rubik pb-[35px] '>{reads} reads</h1>
        <div className=' flex gap-2'>
            <button className=' bg-[#F5B900] text-white py-[10px] px-[35px] rounded-xl text-[18px] font-medium '>Buy Now</button>
            <button className='text-[#F5B900] border-[#F5B900] border-2 bg-white py-[10px] px-[35px] rounded-xl text-[18px] font-medium'>Read Book</button>
        </div>
      </div>
    </div>
    <div className='px-[50px] pt-[57px] pb-[27px] '>
        <h1 className='font-semibold text-[25px] '>About</h1>
        <p className='text-[#626262] font-regular font-rubik '> {desc}</p>
    </div>

    </div>
  )
}

export default bookDetailsCard