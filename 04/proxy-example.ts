// 定義介面
interface IImage {
    display(): void;
}

// 真實物件
class RealImage implements IImage {
    private filename: string;

    constructor(filename: string) {
        this.filename = filename;
        this.loadImageFromDisk();
    }

    private loadImageFromDisk(): void {
        console.log(`載入圖片：${this.filename}`);
    }

    public display(): void {
        console.log(`顯示圖片：${this.filename}`);
    }
}

// 代理物件
class ProxyImage implements IImage {
    private realImage: RealImage | null = null;
    private filename: string;

    constructor(filename: string) {
        this.filename = filename;
    }

    public display(): void {
        // 延遲載入：只有在真正需要時才創建真實物件
        if (this.realImage === null) {
            this.realImage = new RealImage(this.filename);
        }
        this.realImage.display();
    }
}

// 使用範例
const image1 = new ProxyImage("photo1.jpg");
const image2 = new ProxyImage("photo2.jpg");

// 第一次呼叫會載入圖片
console.log("第一次訪問 image1：");
image1.display();

console.log("\n第二次訪問 image1：");
image1.display(); // 不會重複載入

console.log("\n訪問 image2：");
image2.display();